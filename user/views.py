from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Account"])
class LoginTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.LoginTokenSerializer

@extend_schema(tags=["Account"])
class AccountView(APIView):
    serializer_class = (serializers.UserSerializer)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = self.request.user
        account = models.User.objects.get(username=user.username)
        serializer = serializers.UserSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)