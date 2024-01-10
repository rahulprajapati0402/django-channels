import asyncio
import json
import time
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket connected...", event)
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
        for i in range(10):
            self.send({"type": "websocket.send", "text": json.dumps({"count": i})})
            time.sleep(0.5)

    def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket connected...", event)
        await self.send(
            {
                "type": "websocket.accept",
            }
        )

    async def websocket_receive(self, event):
        print("Message received...", event)
        print(event["text"])
        for i in range(10):
            await self.send(
                {
                    "type": "websocket.send",
                    "text": json.dumps({"count": i}),
                }
            )
            await asyncio.sleep(0.5)

    async def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)
        raise StopConsumer()
