import asyncio
import json
import time
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync


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
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "chat.message", "message": event["text"]}
        )
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
        await self.channel_layer.group_send(
            self.group_name, {"type": "chat.message", "message": event["text"]}
        )

    async def chat_message(self, event):
        await self.send({"type": "websocket.send", "text": event["message"]})

    async def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()
