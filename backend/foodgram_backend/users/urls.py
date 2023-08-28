from django.urls import include, path
from rest_framework import routers

from users.views import UserViewSet

router = routers.DefaultRouter()

router.register('users', UserViewSet)
router.regster('users/subsciptions',)
router.register(
    r'users/(?P<user_id>\d+)/subscribe'
)


urlpatterns = [
    path('', include(routers.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
