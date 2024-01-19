from django.urls import path
from .views import index, chat, message_to_group_from_outside_consumer

urlpatterns = [
    path("", index, name="index"),
    path("chat/<str:group_name>/", chat, name="chat_url"),
    path(
        "send-msg/",
        message_to_group_from_outside_consumer,
        name="message_to_group_from_outside_consumer",
    ),
]
