from rest_framework import viewsets, permissions, filters

from django_filters.rest_framework import DjangoFilterBackend

from users.models import UserFollower
from users.serializers import SubscribeSerilizer


class SubscribtionsViewSet(viewsets.ModelViewSet):
    queryset = UserFollower.objects.all()
    serializer_class = SubscribeSerilizer

    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('following__username',)

    def get_queryset(self, *args, **kwargs):
        return (UserFollower.objects.select_related('follower')
                .filter(follower=self.request.user))

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


