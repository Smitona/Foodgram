from api.filters import IngredientFilter, RecipeFilter
from api.pagination import ResultsSetPagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (IngredientListSerializer, RecipeCreateSerializer,
                             RecipeSerializer, TagSerializer)
from django.db.models import Exists, F, OuterRef, Prefetch, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredient, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.serializers import ShortRecipeSerializer


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

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = RecipeFilter

    ordering_fields = ('pub_date', 'name')
    ordering = ('-pub_date',)

    def get_queryset(self, *args, **kwargs):
        recipe_ingr = RecipeIngredient.objects.select_related(
            'ingredient'
        )
        recipes = Recipe.objects.prefetch_related(
            Prefetch('recipe_ingredients', queryset=recipe_ingr),
            'tags'
        ).select_related('author')

        if self.request.user.is_authenticated:
            recipes = recipes.annotate(
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
    def add_del(self, request, Model, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        obj_exists = Model.objects.filter(
            user=self.request.user,
            recipe=pk
        ).exists()
        if request.method == 'POST':
            if obj_exists:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )

            Model.objects.create(
                user=request.user,
                recipe=recipe
            )

            return Response(
                ShortRecipeSerializer(recipe).data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            if not obj_exists:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )
            Model.objects.get(
                user=request.user,
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
        return self.add_del(
            self, request,
            Model=Favorite,
            pk=pk
        )

    @action(
        detail=True, methods=('post', 'delete',),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return self.add_del(
            self, request,
            Model=Cart, pk=pk
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
            recipe__in_cart__user=self.request.user
        )

        groceries = groceries.values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            name=F('ingredient__name'),
            measur_units=F('ingredient__measurement_unit'),
            total=Sum('amount'),
        ).order_by('-name')

        text = 'Список покупок:\n\n' + '\n'.join([
            (f"{food['name']} нужно {food['total']} {food['measur_units']}")
            for food in groceries
        ])

        response = HttpResponse(text, content_type='application/txt')
        response['content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )

        return response
