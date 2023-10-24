from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label='Email', write_only=True
    )
    password = serializers.CharField(
        label='Пароль', write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context['request'], username=email, password=password
            )
            if not user:
                message = 'Email или пароль не верные'
                raise ValidationError(message, code='authorization')
        else:
            message = 'Укажите email и пароль'
            raise ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs
