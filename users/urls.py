from django.urls import path

from users.views.auth import LoginAPIView, LogoutAPIView

app_name = 'users'

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
