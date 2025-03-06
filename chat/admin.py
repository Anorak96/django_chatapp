from django.contrib import admin
from . import models

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', )

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'message', 'sender')