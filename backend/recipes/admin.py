from django.contrib import admin

from recipes.models import (
    Ingredient, Tag, Recipe,
    RecipeTag, RecipeIngredient
)


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(BaseAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class TagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1


@admin.register(Recipe)
class RecipeAmdin(BaseAdmin):
    inlines = [
       IngredientInline,
       TagInline,
    ]
    list_display = (
        'id',
        'author',
        'name',
    )
    list_filter = (
        'author',
    )


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    pass

