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
    path('/set_password/', UserViewSet)
    path('auth/token/login/', name='get_token', )
    path('auth/token/logout/', name='delete_token', )

]