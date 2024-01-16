import asyncio
import json
import time
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from home.models import Chat, Group
from channels.db import database_sync_to_async


class MyWebSocketConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        # self.send(text_data="Message sending to client from server...")
        # self.close()
        for i in range(20):
            self.send(text_data=str(i))
            time.sleep(1)

    def disconnect(self, code):
        return super().disconnect(code)


class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        # await self.send(text_data="Message sending to client from server...")
        # await self.close()
        for i in range(20):
            await self.send(text_data=str(i))
            await asyncio.sleep(1)

    async def disconnect(self, code):
        return super().disconnect(code)


class ChatWebSocketConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.user = self.scope["user"]
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["msg"]
        group = Group.objects.get(name=self.group_name)
        if self.user.is_authenticated:
            Chat.objects.create(group=group, content=message)
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {"type": "chat.message", "message": message}
            )
        else:
            self.send(text_data=json.dumps({"message": "Login required"}))

    def chat_message(self, event):
        self.send(text_data=json.dumps({"message": event["message"]}))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )


class AsyncChatWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        self.user = self.scope["user"]
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["msg"]
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        if self.user.is_authenticated:
            await database_sync_to_async(Chat.objects.create)(
                group=group, content=message
            )
            await self.channel_layer.group_send(
                self.group_name, {"type": "chat.message", "message": message}
            )
        else:
            await self.send(text_data=json.dumps({"message": "Login required"}))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
