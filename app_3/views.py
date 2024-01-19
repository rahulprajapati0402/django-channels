from asgiref.sync import async_to_sync
from django.shortcuts import render, HttpResponse
from channels.layers import get_channel_layer
from home.models import Chat, Group

# Create your views here.


def index(request):
    return render(request, "app_3/index.html")


def chat(request, group_name):
    group = Group.objects.filter(name=group_name).first()
    chats = []
    if not group:
        group = Group.objects.create(name=group_name)
    else:
        chats = Chat.objects.filter(group=group)
    context = {"group_name": group_name, "chats": chats}
    return render(request, "app_3/chat.html", context)


def message_to_group_from_outside_consumer(request):
    group = Group.objects.filter(name="India").first()
    if not group:
        group = Group.objects.create(name="India")
    channel_layer = get_channel_layer()
    print(channel_layer)
    async_to_sync(channel_layer.group_send)(
        group.name,
        {"type": "chat.message", "message": "Hello from outside consumer..."},
    )
    return HttpResponse("Message sent successfully!!")
