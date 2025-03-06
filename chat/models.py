from django.db import models
from user.models import User

class Room(models.Model):
    room_name = models.CharField(max_length=20)
    participants = models.ManyToManyField(User)

    def __str__(self):
        return self.room_name
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='message_room')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    image = models.ImageField(blank=True)
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.room)} - {self.message} - {self.sender}"