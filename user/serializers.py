from rest_framework import serializers
from . import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LoginTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token
    
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ('username', 'password')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = models.User.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user