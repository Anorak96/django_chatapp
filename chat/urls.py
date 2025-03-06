from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('rooms', views.Rooms.as_view(), name='rooms'),
    path('<str:room_name>', views.Room.as_view(), name='room'),
    path('<str:room_name>/messages', views.RoomMessagesView.as_view(), name='room_messages'),
    path('send-message', views.SendMessage.as_view(), name='send_message'),
    path('create', views.CreateRoomApiView.as_view(), name='create_room'),
]
