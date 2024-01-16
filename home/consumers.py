import asyncio
import json
import time
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from .models import Chat, Group


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket connected...", event)
        print("Channel layer", self.channel_layer)
        print("Channel name", self.channel_name)
        async_to_sync(self.channel_layer.group_add)("programmers", self.channel_name)
        self.send(
            {
                "type": "websocket.accept",
            }
        )

    # def websocket_receive(self, event):
    #     print("Message received...", event)
    #     for i in range(10):
    #         self.send({"type": "websocket.send", "text": str(i)})
    #         time.sleep(0.5)

    def websocket_receive(self, event):
        print("Message received...", event)
        async_to_sync(self.channel_layer.group_send)(
            "programmers", {"type": "chat.message", "message": event["text"]}
        )
        # for i in range(10):
        #     self.send({"type": "websocket.send", "text": json.dumps({"count": i})})
        #     time.sleep(0.5)

    def chat_message(self, event):
        self.send({"type": "websocket.send", "text": event["message"]})

    def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)
        async_to_sync(self.channel_layer.group_discard)(
            "programmers", self.channel_name
        )
        raise StopConsumer()


# class MyAsyncConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         print("Websocket connected...", event)
#         await self.send(
#             {
#                 "type": "websocket.accept",
#             }
#         )

#     async def websocket_receive(self, event):
#         print("Message received...", event)
#         print(event["text"])
#         for i in range(10):
#             await self.send(
#                 {
#                     "type": "websocket.send",
#                     "text": json.dumps({"count": i}),
#                 }
#             )
#             await asyncio.sleep(0.5)

#     async def websocket_disconnect(self, event):
#         print("Websocket disconnected...", event)
#         raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket connected...", event)
        print("Channel layer", self.channel_layer)
        print("Channel name", self.channel_name)
        await self.channel_layer.group_add("programmers", self.channel_name)
        await self.send(
            {
                "type": "websocket.accept",
            }
        )

    async def websocket_receive(self, event):
        print("Message received...", event)
        await self.channel_layer.group_send(
            "programmers", {"type": "chat.message", "message": event["text"]}
        )

    async def chat_message(self, event):
        await self.send({"type": "websocket.send", "text": event["message"]})

    async def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)
        await self.channel_layer.group_discard("programmers", self.channel_name)
        raise StopConsumer()


class MySyncConsumerGroup(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket connected...", event)
        print("Channel layer", self.channel_layer)
        print("Channel name", self.channel_name)
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send(
            {
                "type": "websocket.accept",
            }
        )

    def websocket_receive(self, event):
        print("Message received...", event)
        group = Group.objects.get(name=self.group_name)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "chat.message", "message": event["text"]}
        )
        data_dict = json.loads(event["text"])
        Chat.objects.create(content=data_dict["message"], group=group)
        print("Data sent to group", event)

    def chat_message(self, event):
        print("Sending data to client", event)
        self.send({"type": "websocket.send", "text": event["message"]})
        print("Data sent to client", event)

    def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        raise StopConsumer()


class MyAsyncConsumerGroup(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket connected...", event)
        print("Channel layer", self.channel_layer)
        print("Channel name", self.channel_name)
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.send(
            {
                "type": "websocket.accept",
            }
        )

    async def websocket_receive(self, event):
        print("Message received...", event)
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        print(group.name)
        await self.channel_layer.group_send(
            self.group_name, {"type": "chat.message", "message": event["text"]}
        )
        data_dict = json.loads(event["text"])
        await database_sync_to_async(Chat.objects.create)(
            content=data_dict["message"], group=group
        )

    async def chat_message(self, event):
        await self.send({"type": "websocket.send", "text": event["message"]})

    async def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()


class AuthSyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket connected...", event)
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.user = self.scope["user"]
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send(
            {
                "type": "websocket.accept",
            }
        )

    def websocket_receive(self, event):
        if self.user.is_authenticated:
            group = Group.objects.get(name=self.group_name)
            data_dict = json.loads(event["text"])
            data_dict["user"] = self.user.username
            Chat.objects.create(group=group, content=data_dict["message"])
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {"type": "chat.message", "message": data_dict}
            )
        else:
            self.send(
                {
                    "type": "websocket.send",
                    "text": json.dumps({"message": "Login Required", "user": "guest"}),
                }
            )

    def chat_message(self, event):
        self.send({"type": "websocket.send", "text": json.dumps(event["message"])})

    def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        raise StopConsumer()


class AuthAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket connected...", event)
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.user = self.scope["user"]
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.send(
            {
                "type": "websocket.accept",
            }
        )

    async def websocket_receive(self, event):
        if self.user.is_authenticated:
            group = await database_sync_to_async(Group.objects.get)(
                name=self.group_name
            )
            data_dict = json.loads(event["text"])
            data_dict["user"] = self.user.username
            print(data_dict)
            await database_sync_to_async(Chat.objects.create)(
                group=group, content=data_dict["message"]
            )
            await self.channel_layer.group_send(
                self.group_name, {"type": "chat.message", "message": data_dict}
            )
        else:
            await self.send(
                {
                    "type": "websocket.send",
                    "text": json.dumps({"message": "Login Required", "user": "guest"}),
                }
            )

    async def chat_message(self, event):
        await self.send(
            {"type": "websocket.send", "text": json.dumps(event["message"])}
        )

    async def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()
