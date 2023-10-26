from django.contrib.auth.backends import UserModel
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'username', 'first_name', 'last_name', 'patronymic', 'is_staff']
