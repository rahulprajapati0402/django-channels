from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<str:group_name>/", views.group_chat, name="group_chat"),
]
