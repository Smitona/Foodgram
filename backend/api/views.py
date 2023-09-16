from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.serializers import (
    RecipeSeralizer, IngredientSerializer,
    IngredientListSerializer, TagSerializer
)
from recipes.models import Ingredient, Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()

    # filter_backends =
    # search_fields =

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return IngredientSerializer
        return IngredientListSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSeralizer
    permission_classes = (AllowAny,)

    # filter_backends =
    # search_fields =

    def get_ingredients(self, *args, **kwargs):
        ingredient_id = self.kwargs.get('ingredient_id')
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)
        return ingredient

    def get_queryset(self, *artgs, **kwargs):
        ingredients = self.get_ingredients()
        return ingredients.recipies.select_related('author')

    def perform_create(self, serizlier):
        serizlier.save(
            author=self.request.user,
            ingredients=self.get_ingredients()
        )


class ShoppingCartViewSet(viewsets.ModelViewSet):
    pass


class FavoriteViewSet(viewsets.ModelViewSet):
    pass
