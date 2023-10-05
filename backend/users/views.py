from rest_framework import viewsets, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from users.models import CustomUser, UserFollower
from users.serializers import FollowSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    permission_classes = (permissions.IsAuthenticated,)

    #filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    #search_fields = ()

    def get_author(self):
        user_id = self.kwargs.get('user_id')
        author = CustomUser.objects.filter(id=user_id).first()
        return author

    def get_queryset(self, *args, **kwargs):
        return (
            UserFollower.objects.select_related('follower').filter(
                follower=self.get_follower()
            )
        )

    def perform_create(self, serializer):
        serializer.save(
            follower=self.request.user,
            author=self.get_author()
        )
        return Response(
            {'detail': 'Вы успешно подписались на {}'.format(
                self.get_author()
            )},
            status=status.HTTP_201_CREATED
        )

    def delete(self, *args, **kwargs):
        follow = UserFollower.objects.get(
            author=self.get_author(),
            follower=self.request.user
        )
        follow.delete()
        return Response(
            {'detail': 'Вы успешно отписались от {}'.format(
                self.get_author()
            )},
            status=status.HTTP_204_NO_CONTENT
        )


class SubscribeListViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self, *args, **kwargs):
        return CustomUser.objects.filter(
            followers__follower=self.request.user
        )
