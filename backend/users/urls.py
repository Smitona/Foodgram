from django.urls import include, path
from rest_framework import routers

from users.views import SubscribeViewSet, SubscribeListViewSet

router = routers.DefaultRouter()

router.register(
    'users/subscriptions',
    SubscribeListViewSet,
    basename='subscriptions'
)
router.register(
    r'users/(?P<user_id>\d+)/subscribe',
    SubscribeViewSet,
    basename='subscribe'
)

app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),

]
