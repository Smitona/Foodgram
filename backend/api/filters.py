from django_filters import (CharFilter, ChoiceFilter, FilterSet,
                            ModelChoiceFilter, ModelMultipleChoiceFilter)
from recipes.models import Ingredient, Recipe, Tag
from users.models import CustomUser

BOOL_CHOICES = (
    ('0', 'False'),
    ('1', 'True'),
)


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
    )
    is_favorited = ChoiceFilter(
        label='Избранное',
        choices=BOOL_CHOICES,
        method='get_filter_fav'
    )
    is_in_shopping_cart = ChoiceFilter(
        label='Корзина',
        choices=BOOL_CHOICES,
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
            return queryset.filter(in_favorite__user=user)
        return queryset

    def get_filter_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            return queryset.filter(in_cart__user=user)
        return queryset
