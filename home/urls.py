from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<str:group_name>/", views.group_chat, name="group_chat"),
    path("auth/<str:group_name>/", views.auth_chat, name="group_chat"),
]
