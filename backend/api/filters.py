from django_filters import (
    BooleanFilter, CharFilter, ModelMultipleChoiceFilter, FilterSet,
    ModelChoiceFilter, NumberFilter
)
from recipes.models import Ingredient, Recipe, Tag
from users.models import CustomUser


class IngredientFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = (
            'name',
        )


class RecipeFilter(FilterSet):
    author = ModelChoiceFilter(
        queryset=CustomUser.objects.all(),
        label='Автор',
        #field_name='author_id',
    )
    is_favorited = NumberFilter(
        label='Избранное',
        method='get_filter_fav'
    )
    is_in_shopping_cart = BooleanFilter(
        label='Корзина',
        method='get_filter_cart'
    )
    tags = ModelMultipleChoiceFilter(
        label='Тэги',
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug'
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags'
        )

    def get_filter_fav(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            return queryset
        return queryset.filter(in_favorite__user=user)

    def get_filter_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            return queryset
        return queryset.filter(in_cart__user=user)
