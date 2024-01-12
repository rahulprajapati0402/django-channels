from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/sc/", consumers.MySyncConsumer.as_asgi()),
    path("ws/ac/", consumers.MyAsyncConsumer.as_asgi()),
    path("ws/sc/<str:group_name>/", consumers.MySyncConsumerGroup.as_asgi()),
    path("ws/ac/<str:group_name>/", consumers.MyAsyncConsumerGroup.as_asgi()),
]
