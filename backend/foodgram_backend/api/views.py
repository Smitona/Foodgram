from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.serializers import (
    RecipeSeralizer, IngridientSerializer,
    IngridientListSerializer, TagSerializer
)
from recipes.models import Ingredient, Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngridientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()

    # filter_backends =
    # search_fields =

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return IngridientSerializer
        return IngridientListSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSeralizer
    permission_classes = (AllowAny,)

    # filter_backends =
    # search_fields =

    def get_ingridients(self, *args, **kwargs):
        ingridient_id = self.kwargs.get('ingridient_id')
        ingridient = get_object_or_404(Ingredient, id=ingridient_id)
        return ingridient

    def get_queryset(self, *artgs, **kwargs):
        ingridients = self.get_ingridients()
        return ingridients.recipies.select_related('author')

    def perform_create(self, serizlier):
        serizlier.save(
            author=self.request.user,
            ingridients=self.get_ingridients()
        )


class ShoppingCartViewSet(viewsets.ModelViewSet):
    pass


class FavoriteViewSet(viewsets.ModelViewSet):
    pass
