from rest_framework import viewsets

from users.models import UserFollower
from users.serializers import SubsctibeSerilizer


class SubscribtionsViewSet(viewsets.ModelViewSet):
    queryset = UserFollower.objects.all()
    serializer_class = SubsctibeSerilizer

