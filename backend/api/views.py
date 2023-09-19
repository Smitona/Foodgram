from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from api.serializers import (
    RecipeSerializer, RecipeCreateSerializer,
    IngredientListSerializer, TagSerializer
)
from recipes.models import Ingredient, Tag, Recipe


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientListSerializer

    # filter_backends =
    # search_fields =


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)

    # filter_backends =
    # search_fields =

    def get_queryset(self, *artgs, **kwargs):
        queryset = Recipe.objects.all().select_related(
            'author').prefetch_related(
                'ingredients',
            )
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )

'''
    @action(
        detail=True, methods=('post','delete',)
    )
    def favorite(self, request, pk):
        pass
    
    @action(
        detail=True, methods=('post','delete',)
    )
    def shopping_cart(self, request, pk):
        pass
'''