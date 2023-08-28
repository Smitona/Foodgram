from django.urls import include, path
from rest_framework import routers

from users.views import #RecipeViewset

router = routers.DefaultRouter()

router.register('recipes', RecipeViewset)
router.register('recipes/download_shopping_cart',)
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    ShoppingCartViewset,
    basename='cart',
)
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite/',
    FavoriteViewSet,
    basemane='favorite',
)

urlpatterns = [
    path('', include(router.urls))
]