from django.contrib.auth import login, logout
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers.auth import LoginSerializer


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def get_serializer(self, **kwargs):
        context = self.get_serializer_context()
        return LoginSerializer(context=context, **kwargs)

    def get_serializer_context(self):
        context = {'request': self.request, 'view': self}
        return context

    @swagger_auto_schema(tags=['Auth'], operation_summary='Логин', responses={

    })
    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):

    @swagger_auto_schema(tags=['Auth'], operation_summary='Выход', responses={

    })
    def get(self, request: Request, *args, **kwargs):
        logout(request=request)
        return Response(None, status=status.HTTP_200_OK)
