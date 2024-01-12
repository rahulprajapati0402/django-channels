from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "index.html")


def group_chat(request, group_name):
    context = {"group_name": group_name}
    return render(request, "group_chat.html", context)
