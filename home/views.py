from django.shortcuts import render
from .models import Chat, Group

# Create your views here.


def home(request):
    return render(request, "index.html")


def group_chat(request, group_name):
    group = Group.objects.filter(name=group_name).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group=group)
    else:
        Group.objects.create(name=group_name)
    context = {"group_name": group_name, "chats": chats}
    return render(request, "group_chat.html", context)
