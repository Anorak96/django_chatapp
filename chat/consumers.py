import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from . import models, serializers
from user.models import User

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name =f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(
            self.room_name, 
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_name, 
            self.channel_name
        )
        self.close(code)

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json

        event = {
            "type": "send_message",
            "message": message
        }
        await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event):
        data = event["message"]
        await self.create_message(data=data)

        response = {
            "sender": data['sender']['username'],
            "message": data['message'],
            "room": data['room']
        }
        await self.send(text_data=json.dumps({"message": response}))

    @database_sync_to_async
    def create_message(self, data):
        print(data)
        get_room = models.Room.objects.get(room_name=data['room'])
        sender_ = User.objects.get(username=data['sender']['username'])
        if not models.Message.objects.filter(message=data['message']).exists():
            new_message = models.Message.objects.create(room=get_room, sender=sender_, message=data['message'])
