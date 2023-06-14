from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username')

class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')