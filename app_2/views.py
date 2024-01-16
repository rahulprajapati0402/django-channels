from django.shortcuts import render
from home.models import Chat, Group

# Create your views here.


def index(request):
    return render(request, "app/index.html")


def chat_app(request, group_name):
    group = Group.objects.filter(name=group_name).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group=group)
    else:
        Group.objects.create(name=group_name)
    context = {"group_name": group_name, "chats": chats}
    return render(request, "app/chat.html", context)
