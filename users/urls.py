from django.urls import path

from users.views.auth import LoginAPIView, LogoutAPIView, RegisterAPIView, PasswordChangeAPI

app_name = 'users'

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('password-change/', PasswordChangeAPI.as_view(), name='password_change'),
]
