from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredient, RecipeTag, Tag)


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
    min_num = 1
    extra = 1


class TagInline(admin.TabularInline):
    model = RecipeTag
    min_num = 1
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
        'image_tag',
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
            favorited_count=Count('in_favorite__recipe')
        )

    def favorited_count(self, obj):
        return obj.favorited_count

    def image_tag(self, obj):
        return format_html(
            '<img src="{}" width=auto height="30" />'.format(obj.image.url)
        )


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }
    list_display = (
        'name',
        'color'
    )


@admin.register(Favorite)
class FavoriteAdmin(BaseAdmin):
    pass


@admin.register(Cart)
class CartAdmin(BaseAdmin):
    pass
