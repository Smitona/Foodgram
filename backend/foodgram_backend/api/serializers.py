from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from recipes.models import Recipe, Ingredient, Tag


class RecipeSeralizer(serializers.ModelSeializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    # is_favorited = serializers.
    is_in_shopping_cart = serializers.SerializerMethodField

    class Meta:
        Model = Recipe
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method == 'POST':
            recipe_id = self.context.get('view').kwargs.get('recipe_id')
            recipe = get_object_or_404(Recipe, pk=recipe_id)
            author = self.context['request'].user

        if Recipe.objects.filter(name=recipe, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже создали рецепт с таким названием!',
            )
        return data

"""     def get_is_favorited(self):
        pass """


class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngridientListSerializer(IngridientSerializer):
    class Meta:
        model = Ingredient
        fields = IngridientSerializer.Meta.fields


class ShoppingCart(serializers.ModelSerializer):
    pass


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fileds = (
            'id',
            'name',
            'color',
            'slug',
        )

