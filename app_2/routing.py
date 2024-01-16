from django.urls import path
from .consumers import (
    MyWebSocketConsumer,
    MyAsyncWebsocketConsumer,
    ChatWebSocketConsumer,
    AsyncChatWebSocketConsumer,
)

app_websocket_urlpatterns = [
    path("ws/wsc/", MyWebSocketConsumer.as_asgi()),
    path("ws/awsc/", MyAsyncWebsocketConsumer.as_asgi()),
    path("ws/chat/wsc/<str:group_name>/", ChatWebSocketConsumer.as_asgi()),
    path("ws/chat/awsc/<str:group_name>/", AsyncChatWebSocketConsumer.as_asgi()),
]
