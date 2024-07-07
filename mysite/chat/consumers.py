import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        username = self.scope['user'].username
        user_pk = self.scope['user'].pk
        message = "<Connected. Say Hi!>"
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": message,
                "username": username,
                "user_pk": user_pk,
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        username = self.scope['user'].username
        user_pk = self.scope['user'].pk
        message = "<Disconnected>"
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": message,
                "username": username,
                "user_pk": user_pk,
            }
        )

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        from pprint import pprint
        pprint(text_data_json)
        received_type = text_data_json["type"]
        message = text_data_json["message"]
        username = self.scope['user'].username
        user_pk = self.scope['user'].pk

        if received_type == 'message':
            event_type = 'chat.message'
            message_username = username
        elif received_type == 'name_change':
            event_type = 'chat.name_change'
            new_username = text_data_json['username']
            message_username = await self.change_username(self.scope['user'], new_username)
        print(f"message: {message}")
        print(f"username: {username}")
        print(f"user_pk: {user_pk}")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": event_type,
                "message": message,
                "username": message_username,
                "user_pk": user_pk,
            }
        )

    @database_sync_to_async
    def change_username(self, user, new_username):
        user.username = new_username
        try:
            user.save(update_fields=['username'])
            return new_username
        except:
            return user.username

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        user_pk = event["user_pk"]
        event_type = event["type"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "type": event_type,
            "message": message,
            "username": username,
            "user_pk": user_pk,
        }))

    async def chat_name_change(self, event):
        message = event["message"]
        username = event["username"]
        user_pk = event["user_pk"]
        event_type = event["type"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "type": event_type,
            "message": message,
            "username": username,
            "user_pk": user_pk,
        }))
