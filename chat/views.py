from django.shortcuts import render, redirect, get_object_or_404
from user.serializers import UserSerializer
from user.models import User
from . import models, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Chat'])
class CreateRoomApiView(APIView):
    serializer_class = serializers.CreateRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.CreateRoomSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Chat'])
class Room(APIView):
    serializer_class = serializers.RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, room_name):
        room_ = get_object_or_404(
            models.Room.objects.prefetch_related('message_room', 'participants'),
            room_name=room_name
        )
        serializer = serializers.RoomSerializer(room_)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Chat'])
class Rooms(APIView):
    serializer_class = serializers.RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = self.request.user
        account = User.objects.get(username=user.username)
        rooms = models.Room.objects.filter(participants=account)
        serializer = serializers.RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Chat"])
class RoomMessagesView(APIView):
    serializer_class = serializers.MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, room_name):
        room = models.Room.objects.get(room_name=room_name)
        messages = models.Message.objects.filter(room=room)
        serializer = serializers.MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@extend_schema(tags=["Chat"])
class SendMessage(APIView):
    serializer_class = serializers.CreateMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.CreateMessageSerializer(data=request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)