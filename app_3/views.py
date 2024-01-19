from django.shortcuts import render
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
