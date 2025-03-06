from rest_framework import serializers
from . import models
from user import serializers as ser

class MessageSerializer(serializers.ModelSerializer):
    sender = ser.UserSerializer()

    class Meta:
        model = models.Message
        fields = ['id', 'room', 'sender', 'message', 'image', 'sent']
        extra_kwargs = {'id': {'read_only': True}, 'sent': {'read_only': True}}
        
class RoomSerializer(serializers.ModelSerializer):
    # messages = MessageSerializer(many=True, read_only=True)
    participants = ser.UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Room
        fields = ('id', 'room_name', 'participants')
        depth = 1

class CreateRoomSerializer(serializers.ModelSerializer):
    participants = ser.UserSerializer(write_only=True, required=False, many=True, allow_null=True)

    class Meta:
        model = models.Room
        fields = ['room_name', 'participants']

    def create(self, validated_data):
        user = self.context['request'].user

        room = models.Room.objects.create(
            room_name = validated_data['room_name'],
        )
        room.participants.add(user)
        return room
    
class CreateMessageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True, required=False)
    room = RoomSerializer(read_only=True, required=False)
    sender = ser.UserSerializer(read_only=True, required=False)
    message = serializers.CharField()

    class Meta:
        model = models.Message
        fields = ['room', 'sender', 'message', 'image']

    def create(self, validated_data):
        sender = self.context['request'].user
        room = self.context['room']

        message = models.Message.objects.create(
            room = room,
            sender = sender,
            message = validated_data['message'],
            image = validated_data['image']
        )
        message.save()
        return message
