from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("chat/<str:group_name>/", views.chat_app, name="chat"),
]
