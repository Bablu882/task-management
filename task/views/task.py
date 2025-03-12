from ast import Is
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from task.models.task import UserTask, PushSubscription
from task.serializers.task import UserTaskSerializer, CompleteTaskSerializer, SearchUserTaskSerializer, \
    SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils import timezone
from pywebpush import webpush, WebPushException
import json
from django.conf import settings


class UserTaskCreateView(generics.CreateAPIView):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)
        assigned_user_id = task.assigned_to.id
        
        if assigned_user_id:
            NotificationService.send_push_notification(
                user_ids=[assigned_user_id],
                title="New Task Assigned",
                message=f"You have been assigned a new task: {task.id}",
                pvt_key=settings.VAPID_PRIVATE_KEY,
                vapid_email=settings.VAPID_EMAIL,
            )


class CompleteTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = UserTask.objects.get(pk=pk)
        except UserTask.DoesNotExist:
            return Response({"non_field_errors": ["Task not found."]}, status=status.HTTP_404_NOT_FOUND)

        if task.assigned_to != request.user:
            return Response({"non_field_errors": ["You cannot complete a task that is not assigned to you."]}, status=status.HTTP_403_FORBIDDEN)

        task.is_completed = True
        task.completed_on = timezone.now()
        task.status = 'completed'
        task.save()
        NotificationService.send_push_notification(
                user_ids=[task.created_by.id],  
                title="Task Completed",
                message=f"The task '{task.id}' has been completed by {request.user.name}.",
                pvt_key=settings.VAPID_PRIVATE_KEY,
                vapid_email=settings.VAPID_EMAIL,
            )
        serializer = CompleteTaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        try:
            task = UserTask.objects.get(pk=pk)
        except UserTask.DoesNotExist:
            return Response({"non_field_errors": ["Task not found."]}, status=status.HTTP_404_NOT_FOUND)
        
        if task.status == 'pending':
            return Response({"non_field_errors": ["Pending task can not be deleted."]}, status=status.HTTP_403_FORBIDDEN)

        if task.created_by != request.user:
            return Response({"non_field_errors": ["Only task owner can delete the task"]}, status=status.HTTP_403_FORBIDDEN)

        task.delete()
        return Response({"success_message": ["Task deleted."]}, status=status.HTTP_204_NO_CONTENT)
    

class GetAllTaskView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SearchUserTaskSerializer
    queryset = UserTask.objects.all()



class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        already = PushSubscription.objects.filter(
            user=request.user,
            endpoint=serializer.validated_data['endpoint']
        ).first()

        if already:
            return Response(
            {
                "success_message": ["Subscription created successfully."],
                "subscription": [SubscriptionSerializer(already).data],
            },
            status=status.HTTP_201_CREATED
        )

        subscription = PushSubscription.objects.create(
            user=request.user,
            endpoint=serializer.validated_data['endpoint'],
            auth_key=serializer.validated_data['auth_key'],
            p256dh_key=serializer.validated_data['p256dh_key'],
        )

        return Response(
            {
                "success_message": ["Subscription created successfully."],
                "subscription": [SubscriptionSerializer(subscription).data],
            },
            status=status.HTTP_201_CREATED)
    



class NotificationService:
    """ Service class for handling notifications. """

    @staticmethod
    def delete_subscriber(url: str):
        """Deletes push subscription based on URL."""
        PushSubscription.objects.filter(endpoint=url).delete()

    @staticmethod
    def _notify(endpoint: str, hash_: str, auth: str, title: str, body: str, pvt_key: str, vapid_email: str):
        """Handles sending push notifications to a specific endpoint."""
        try:
            webpush(
                subscription_info={"endpoint": endpoint, "keys": {"p256dh": hash_, "auth": auth}},
                data=json.dumps({"code": title, "body": body}),
                vapid_private_key=pvt_key,
                vapid_claims={"sub": f"mailto:{vapid_email}"},
            )
        except WebPushException as e:
            if e.response.status_code in (410, 403):  # Subscription expired or forbidden
                NotificationService.delete_subscriber(endpoint)

    def send_push_notification(user_ids, title, message, pvt_key, vapid_email):
        """ Sends push notifications to all subscribed users """
        subscriptions = PushSubscription.objects.filter(user_id__in=user_ids)

        if not subscriptions.exists():
            return {"non_field_errors": ["No push subscriptions found for these users."]}

        failed_subscriptions = []

        for subscription in subscriptions:
            try:
                NotificationService._notify(subscription.endpoint, subscription.p256dh_key, subscription.auth_key, title, message, pvt_key, vapid_email)
            except Exception as e:
                failed_subscriptions.append(subscription.endpoint)

        response_data = {"success": True, "failed_subscriptions": failed_subscriptions}
        return response_data if failed_subscriptions else {"success_message": ["Notification sent successfully"]}