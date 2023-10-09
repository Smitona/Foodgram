from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from api.serializers import (
    RecipeSerializer, RecipeCreateSerializer,
    IngredientListSerializer, TagSerializer,
    ShortRecipeSerializer
)
from api.permissions import AuthorOrReadOnly
from api.pagination import ResultsSetPagination

from recipes.models import Ingredient, Tag, Recipe, Favorite


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientListSerializer
    pagination_class = None

    # filter_backends =
    # search_fields =


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          AuthorOrReadOnly,)
    pagination_class = ResultsSetPagination

    # filter_backends =
    # search_fields =

    def get_queryset(self, *args, **kwargs):
        recipes = Recipe.objects.select_related(
            'author').prefetch_related(
                'ingredients',
            )
        return recipes

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )

    @staticmethod
    def add_to(self, Model, message, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        Model.objects.create(
                user=self.request.user,
                recipe=recipe
            )

        return Response(
                {'detail': message},
                ShortRecipeSerializer(recipe).data,
                status=status.HTTP_201_CREATED
            )

    @staticmethod
    def delete_from(self, Model, message, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        Model.objects.get(
                user=self.request.user,
                recipe=recipe
            ).delete()

        return Response(
            {'detail': message},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=True, methods=('post', 'delete',)
    )
    def favorite(self, request, **kwargs):

        if request.method == 'POST':
            self.add_to(
                self, Model=Favorite,
                message='Рецепт теперь в избранном'
            )

        if request.method == 'DELETE':
            self.delete_from(
                self, Model=Favorite,
                message='Рецепт удалён из избранного'
            )
'''
    @action(
        detail=True, methods=('post','delete',)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            self.add_to(
                self, Model=Cart,
                message='Рецепт теперь в корзине'
            )

        if request.method == 'DELETE':
            self.delete_from(
                self, Model=Cart,
                message='Рецепт удалён из корзины'
            )

    @action(
        detail=True, methods=('post','delete',)
    )     
    def download_shopping_cart(self, request):
        groceries = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        )
        groceries = groceries.filter(
            
        )

'''

