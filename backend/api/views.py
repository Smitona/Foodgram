from django.shortcuts import get_object_or_404
from django.db.models import Exists, OuterRef, Sum, F
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
)

from api.filters import IngredientFilter, RecipeFilter
from api.serializers import (
    RecipeSerializer, RecipeCreateSerializer,
    IngredientListSerializer, TagSerializer,
    ShortRecipeSerializer
)
from api.permissions import AuthorOrReadOnly
from api.pagination import ResultsSetPagination

from recipes.models import (
    Ingredient, RecipeIngredient, Tag, Recipe, Favorite, Cart
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientListSerializer
    pagination_class = None

    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,
                          AuthorOrReadOnly,)
    pagination_class = ResultsSetPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self, *args, **kwargs):
        queryset = Recipe.objects.select_related(
            'author').prefetch_related(
                'ingredients',
            )
        recipes = queryset.annotate(
            is_favorited=Exists(
                Favorite.objects.filter(
                    user=self.request.user,
                    recipe__pk=OuterRef('pk')
                )
            ),
            is_in_shopping_cart=Exists(
                Cart.objects.filter(
                    user=self.request.user,
                    recipe__pk=OuterRef('pk')
                )
            )
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
    def add_to(self, Model, pk):
        if Model.objects.filter(
            user=self.request.user,
            recipe=pk
        ).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, pk=pk)
        Model.objects.create(
                user=self.request.user,
                recipe=recipe
            )

        return Response(
                ShortRecipeSerializer(recipe).data,
                status=status.HTTP_201_CREATED
            )

    @staticmethod
    def delete_from(self, Model, pk):
        if not Model.objects.filter(
            user=self.request.user,
            recipe=pk
        ).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, pk=pk)
        Model.objects.get(
                user=self.request.user,
                recipe=recipe
            ).delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=True, methods=('post', 'delete',),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):

        if request.method == 'POST':
            return self.add_to(
                self, Model=Favorite,
                pk=pk
            )

        if request.method == 'DELETE':
            return self.delete_from(
                self, Model=Favorite,
                pk=pk
            )

    @action(
        detail=True, methods=('post', 'delete',),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to(
                self, Model=Cart,
                pk=pk
            )

        if request.method == 'DELETE':
            return self.delete_from(
                self, Model=Cart,
                pk=pk
            )

    @action(
        detail=False, methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        groceries = RecipeIngredient.objects.select_related(
            'recipe', 'ingredient'
        )
        groceries = groceries.filter(
            recipe__cart__user=request.user
        )

        groceries = groceries.values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            name=F('ingredient__name'),
            measur_units=F('ingredient__measurement_unit'),
            total=Sum('amount'),
        ).order_by('-ingredient__name')

        text = 'Список покупок:\n\n' + '\n'.join([
            (f"{food['name']} нужно {food['total']} {food['measur_units']}")
            for food in groceries
        ])

        response = HttpResponse(text, content_type='application/txt')
        response['content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )

        return response
