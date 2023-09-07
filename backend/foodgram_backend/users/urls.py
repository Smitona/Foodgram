from django.urls import include, path
from rest_framework import routers

from users.views import SubscribtionsViewSet

router = routers.DefaultRouter()

router.register('users/subsciptions', SubscribtionsViewSet)
router.register(
    r'users/(?P<user_id>\d+)/subscribe', SubscribtionsViewSet
)

app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
