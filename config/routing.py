from django.urls import path
from coordinat import consumers

websocket_urlpatterns = [
    path('ws/coordinat/', consumers.CoordinatesConsumer.as_asgi())
]
