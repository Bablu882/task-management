from random import choice
from turtle import mode
from django.db import models
from task.models.user import User


class UserTask(models.Model):

    STATUS = (
          ('pending', 'PENDING'),
          ('completed', 'COMPLETED')
     )
    
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tasks_created_by', null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tasks_assign_to')
    desc = models.TextField()
    deadline = models.DateField()
    completed_on = models.DateTimeField(null=True)
    status = models.CharField(choices=STATUS, max_length=10, default='pending')
