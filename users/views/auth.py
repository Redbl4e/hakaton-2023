from django.contrib.auth import login, logout

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from docs.schemas import error_schema
from docs.users.schemas import user_schema
from users.models import User
from users.serializers.auth import UserLoginSerializer, UserRegisterSerializer, PasswordChangeSerializer
from users.serializers.profile import UserSerializer


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def get_serializer(self, **kwargs):
        context = self.get_serializer_context()
        return UserLoginSerializer(context=context, **kwargs)

    def get_serializer_context(self):
        context = {'request': self.request, 'view': self}
        return context

    @swagger_auto_schema(tags=['Auth'], operation_summary='Логин', responses={
        status.HTTP_200_OK: '',
        status.HTTP_400_BAD_REQUEST: error_schema
    }, operation_description='Отдаёт Set-Cookie с session_id')
    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):

    @swagger_auto_schema(tags=['Auth'], operation_summary='Выход', responses={
        status.HTTP_200_OK: '',
    })
    def get(self, request: Request, *args, **kwargs):
        logout(request=request)
        return Response(None, status=status.HTTP_200_OK)


class RegisterAPIView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(tags=['Auth'], operation_summary='Регистрация', responses={
        status.HTTP_201_CREATED: user_schema,
        status.HTTP_400_BAD_REQUEST: error_schema
    })
    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_201_CREATED)


class PasswordChangeAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    @swagger_auto_schema(
        tags=['Auth'], responses={
            status.HTTP_204_NO_CONTENT: '',
            status.HTTP_400_BAD_REQUEST: error_schema,
            status.HTTP_401_UNAUTHORIZED: error_schema
        }, operation_summary='Сменить пароль')
    def put(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, serializer.validated_data)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
