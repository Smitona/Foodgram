from django.contrib import admin

from recipes.models import (
    Ingredient, Tag, Recipe,
    RecipeTags, RecipeIngredients
)


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(BaseAdmin):
    pass


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    pass


@admin.register(Recipe)
class RecipeAmdin(BaseAdmin):
    pass


@admin.register(RecipeTags)
class RecipeTag(BaseAdmin):
    pass


@admin.register(RecipeIngredients)
class RecipeIngredients(BaseAdmin):
    pass
