from django.urls import include, path
from rest_framework import routers

from api.views import (
    RecipeViewSet, IngredientViewSet, TagViewSet
)

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    'recipes',
    RecipeViewSet,
    basename='recipes',
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
