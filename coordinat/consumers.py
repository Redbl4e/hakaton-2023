import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from coordinat.serializers import UpdateCoordinateSerializer


class CoordinatesConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = await self.decode_json(text_data)
        await self.update_data(data)
        response_data = {
            'message': 'Received latitude and longitude successfully.'
        }
        await self.send(text_data=await self.encode_json(response_data))

    @sync_to_async(thread_sensitive=True)
    def update_data(self, data):
        serializer = UpdateCoordinateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.update(instance=serializer.validated_data.pop("user_id"),
                                 validated_data=serializer.validated_data)
        return data

    @classmethod
    async def decode_json(cls, text_data):
        return json.loads(text_data)

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(content)
