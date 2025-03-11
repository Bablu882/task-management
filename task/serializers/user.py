from rest_framework import serializers
from task.models.user import User
from django.contrib.auth import authenticate
from task.utils import CustomDateTimeField


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['name', 'number', 'email', 'password']

    def validate(self, data):
        number = data.get('number')

        if not number.isdigit():
            raise serializers.ValidationError({"number": ["This field should contain only digits."]})
        
        if len(number) != 10:
            raise serializers.ValidationError({"number":["this field should be 10 digits"]})         

        return data
    
    def create(self, validated_data):
        user = User(
            name=validated_data['name'],
            number=validated_data['number'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    


class LoginSerializer(serializers.Serializer):
    number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        number = data.get('number')
        password = data.get('password')

        user = authenticate(number=number, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data    
    

class UserSerializer(serializers.ModelSerializer):
    created_on = CustomDateTimeField()

    class Meta:
        model = User
        fields = ['id', 'name', 'number', 'email', 'created_on']    