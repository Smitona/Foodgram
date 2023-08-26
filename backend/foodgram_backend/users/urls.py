from django.urls import include, path
from rest_framework import routers

from users.views import #Viewsets

router = routers.DefaultRouter()

router.register('users', Viewset)
router.regster('users/subsciptions',)
router.register(
    r'users/(?P<user_id>\d+)/subscribe'
)


urlpatterns = [
    path('', include(routers.urls)),
    path('/me/', )
    path('/set_password/', )
    path('auth/token/login/', name='get_token')
    path('auth/token/logout/', name='delete_token')

]