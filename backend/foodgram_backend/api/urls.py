from django.urls import include, path
from rest_framework import routers

from api.views import (
    RecipeViewSet, IngridientViewSet, ShoppingCartViewSet, FavoriteViewSet
)

router = routers.DefaultRouter()

router.register('recipes', RecipeViewSet)
router.register('recipes/download_shopping_cart',)
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    ShoppingCartViewSet,
    basename='cart',
)
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite/',
    FavoriteViewSet,
    basemane='favorite',
)
router.register(
    'ingridients',
    IngridientViewSet,
    basename='ingridients'
)

urlpatterns = [
    path('', include(router.urls))
]