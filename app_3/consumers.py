import asyncio
import time
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from home.models import Chat, Group


class MyJsonWebsocketConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        # self.close()

    def receive_json(self, content, **kwargs):
        print(content)
        for i in range(10):
            self.send_json({"message": str(i)})
            time.sleep(1)

    def disconnect(self, code):
        return super().disconnect(code)


class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # await self.close()

    async def receive_json(self, content, **kwargs):
        print(content)
        for i in range(10):
            await self.send_json({"message": str(i)})
            await asyncio.sleep(1)

    async def disconnect(self, code):
        return super().disconnect(code)


class ChatJsonWebsocketConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.user = self.scope["user"]
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()
        # self.close()

    def receive_json(self, content, **kwargs):
        print(content)
        if self.user.is_authenticated:
            group = Group.objects.get(name=self.group_name)
            Chat.objects.create(group=group, content=content["msg"])
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {"type": "chat.message", "message": content["msg"]}
            )
        else:
            self.send_json({"message": "You are not authenticated"})

    def chat_message(self, event):
        self.send_json({"message": event["message"]})

    def disconnect(self, code):
        return super().disconnect(code)


class ChatAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.user = self.scope["user"]
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def receive_json(self, content, **kwargs):
        print(content)
        if self.user.is_authenticated:
            group = await database_sync_to_async(Group.objects.get)(
                name=self.group_name
            )
            await database_sync_to_async(Chat.objects.create)(
                group=group, content=content["msg"]
            )
            await self.channel_layer.group_send(
                self.group_name, {"type": "chat.message", "message": content["msg"]}
            )
        else:
            await self.send_json({"message": "You are not authenticated"})

    async def chat_message(self, event):
        await self.send_json({"message": event["message"]})

    async def disconnect(self, code):
        return super().disconnect(code)
