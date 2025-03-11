from rest_framework import serializers
from task.models.task import UserTask
from task.models.user import User
from task.utils import CustomDateTimeField
from task.serializers.user import UserSerializer


class UserTaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserTask
        fields = ['id', 'created_by', 'assigned_to', 'desc', 'deadline', 'status']


class CompleteTaskSerializer(serializers.ModelSerializer):
    created_on = CustomDateTimeField()
    completed_on = CustomDateTimeField()

    class Meta:
        model = UserTask
        fields = '__all__'

    def validate(self, data):
        # Ensuring that the task can only be completed if assigned to the current user
        task = self.instance  # The task instance we are updating
        if task.assigned_to != self.context['request'].user:
            raise serializers.ValidationError("You cannot complete a task that is not assigned to you.")
        return data



class SearchUserTaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    assigned_to = UserSerializer()
    created_on = CustomDateTimeField()
    completed_on = CustomDateTimeField()
    deadline = CustomDateTimeField()

    class Meta:
        model = UserTask
        fields = '__all__'