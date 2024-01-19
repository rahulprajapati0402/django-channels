from django.urls import path
from .views import index, chat

urlpatterns = [
    path("", index, name="index"),
    path("chat/<str:group_name>/", chat, name="chat_url"),
]
