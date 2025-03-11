from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from task.models.task import UserTask
from .utils import send_socket_notification


@receiver(post_save, sender=UserTask)
def when_create_user_notification(sender, instance, created, **kwargs):
    if created:
        message = "A new task has beed assigned to you."
        code = 'new_notification'
        print(instance.assigned_to.id)
        send_socket_notification([instance.assigned_to.id], code, message)
    else:
        if instance.status == 'completed':
            message = "Your task has been marked as completed."
            code = 'new_notification'
            send_socket_notification([instance.created_by.id], code, message)    