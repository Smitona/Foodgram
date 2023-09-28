from rest_framework import viewsets, permissions, filters

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from users.models import CustomUser, UserFollower
from users.serializers import SubscribeSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer

    permission_classes = (permissions.IsAuthenticated,)

    #filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    #search_fields = ()

    def get_queryset(self, *args, **kwargs):
        return (
            UserFollower.objects.select_related('follower').filter(
                follower=CustomUser.objects.get(username=self.request.user)
            )
        )

    def get_author(self):
        user_id = self.kwargs.get('user_id')
        author = CustomUser.objects.filter(id=user_id).first()
        return author

    def perform_create(self, serializer):
        serializer.save(
            follower=CustomUser.objects.get(username=self.request.user),
            author=self.get_author()
        )


class SubscribeListViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer

    def get_queryset(self, *args, **kwargs):
        return (
            UserFollower.objects.select_related('follower').filter(
                follower=CustomUser.objects.get(username=self.request.user)
            )
        )
