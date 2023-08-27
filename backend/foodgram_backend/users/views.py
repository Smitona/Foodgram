from rest_framework import serializers, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import UserSerializer

class SignUpView:
    pass

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    

    def me(self, request):
        pass    
