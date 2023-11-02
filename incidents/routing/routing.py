from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from . import consumers
from websoket import YourConsumer

websocket_urlpatterns = [
    path('ws/coordinats/', consumers.YourConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
