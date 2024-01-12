from django.contrib import admin
from .models import Chat, Group

# Register your models here.


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["pk", "content", "time_stamp", "group"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
