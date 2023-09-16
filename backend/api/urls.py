from django.urls import include, path
from rest_framework import routers

from api.views import (
    RecipeViewSet, IngredientViewSet, ShoppingCartViewSet,
    FavoriteViewSet, TagViewSet
)

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    'recipes',
    RecipeViewSet,
    basename='recipes',
)
router.register(
    'recipes/download_shopping_cart',
    ShoppingCartViewSet,
    basename='download_cart'
)
router.register(
    r'recipes/(?P<recipe_id>\d+)/is_in_shopping_cart',
    ShoppingCartViewSet,
    basename='cart',
)
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite/',
    FavoriteViewSet,
    basename='favorite',
)
router.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients'
)

router.register(
    'tags',
    TagViewSet,
    basename='tags'
)

urlpatterns = [
    path('', include(router.urls))
]
