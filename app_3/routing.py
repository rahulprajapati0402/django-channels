from django.urls import path
from .consumers import (
    MyJsonWebsocketConsumer,
    MyAsyncJsonWebsocketConsumer,
    ChatAsyncJsonWebsocketConsumer,
    ChatJsonWebsocketConsumer,
)

ws_patterns = [
    path("ws/jwsc/", MyJsonWebsocketConsumer.as_asgi()),
    path("ws/ajwsc/", MyAsyncJsonWebsocketConsumer.as_asgi()),
    path("ws/jwsc/<str:group_name>/", ChatJsonWebsocketConsumer.as_asgi()),
    path("ws/ajwsc/<str:group_name>/", ChatAsyncJsonWebsocketConsumer.as_asgi()),
]
