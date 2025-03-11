from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from task.models.task import UserTask
from task.serializers.task import UserTaskSerializer, CompleteTaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils import timezone


class UserTaskCreateView(CreateAPIView):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


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