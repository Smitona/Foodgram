from django.db import IntegrityError

from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import UserSerializer, UserCreateSerializer, UserMeSerializer


class SignUpView(APIView):
    permissions_classes = (AllowAny,)
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            CustomUser.objects.get_or_create(
                email=serializer.validated_data.get('email'),
                username=serializer.validated_data.get('username'),
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'Пользователь с такой почтой уже зарегистрирован.',
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserMeSerializer,
    )
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            user = self.request.user
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    permissions_classes = (AllowAny,)
    serializer_class = UserCreateSerializer
