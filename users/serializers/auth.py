from django.contrib.auth import authenticate
from django.contrib.auth.backends import UserModel
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from fcm_django.models import FCMDevice

from exceptions import ValidationError
from users.models import User, Coordinate


class UserLoginSerializer(serializers.Serializer):
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


class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = ('name', 'device_id', 'device_id',
                  'registration_id', 'type')


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        label='Email'
    )
    password1 = serializers.CharField(label='Пароль')
    password2 = serializers.CharField(label='Подтверждение пароля')
    device_data = FCMDeviceSerializer(label="Токен")

    def create(self, validated_data):
        password = validated_data.pop('password1')
        token_data = validated_data.pop('device_data')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Сoordinate.objects.create(**token_data, user_id=user.id)

        return user

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.pop('password2')

        if password1 != password2:
            raise ValidationError('Пароли должны совпадать', code='authorization')

        try:
            validate_password(password1)
        except DjangoValidationError as e:
            raise ValidationError(e.messages)
        return attrs

    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise ValidationError('Данный email уже занят', code='authorization')
        return value

    def validate_username(self, value):
        if UserModel.objects.filter(username=value).exists():
            raise ValidationError('Данное имя пользователя уже занято', code='authorization')
        return value

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'patronymic', 'username', 'email', 'password1', 'password2',
                  'device_data']


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(label='Старый пароль')
    new_password1 = serializers.CharField(label='Новый пароль')
    new_password2 = serializers.CharField(label='Подтверждение пароля')

    def validate(self, attrs):
        if attrs['new_password1'] != attrs['new_password2']:
            raise ValidationError('Пароли не совпадают')

        try:
            validate_password(attrs['new_password1'])
        except DjangoValidationError as e:
            raise ValidationError(e.messages)

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not check_password(value, user.password):
            raise ValidationError('Указан не верный старый пароль', code='old_password')
        return value

    def update(self, user, validated_data):
        user.password = make_password(validated_data['new_password1'])
        user.save()

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']
