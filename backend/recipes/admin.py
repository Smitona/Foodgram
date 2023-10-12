from django.db.models import Count
from django.contrib import admin

from recipes.models import (
    Ingredient, Tag, Recipe,
    RecipeTag, RecipeIngredient,
    Favorite, Cart
)


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(BaseAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )
    search_fields = ('name',)


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class TagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(BaseAdmin):
    inlines = [
        IngredientInline,
        TagInline,
    ]
    list_display = (
        'id',
        'author',
        'name',
        'favorited_count',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super(RecipeAdmin, self).get_queryset(request)
        return queryset.annotate(
            favorited_count=Count('in_favorite')
        )

    def favorited_count(self, obj):
        return obj.favorited_count


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(BaseAdmin):
    pass


@admin.register(Cart)
class CartAdmin(BaseAdmin):
    pass
