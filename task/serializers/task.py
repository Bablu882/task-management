from rest_framework import serializers
from task.models.task import UserTask, PushSubscription
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
        task = self.instance
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


        
class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    created_on = CustomDateTimeField(required=False)

    class Meta:
        model = PushSubscription
        fields = '__all__'
