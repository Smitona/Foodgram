from drf_extra_fields.fields import Base64ImageField

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import (
    Recipe, Ingredient, Tag, RecipeIngredient, Favorite
)
from users.serializers import CustomUserSerializer, ShortRecipeSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
       source='ingredient.id'
    )
    measurement_unit = serializers.ReadOnlyField(
       source='ingredient.measurement_unit'
    )
    name = serializers.ReadOnlyField(
       source='ingredient.name'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    ingredients = IngredientSerializer(
        read_only=True, many=True,
        source='recipeingredient_set'
    )
    tags = TagSerializer(
        read_only=True, many=True,
    )
    author = CustomUserSerializer(read_only=True)
    text = serializers.SerializerMethodField()
    is_favorited = serializers.BooleanField(
        read_only=True, default=False
    )
    is_in_shopping_cart = serializers.BooleanField(
        read_only=True, default=False
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'image',
            'name',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )
        read_only_fields = ('pub_date',)

    @staticmethod
    def get_text(obj):
        return obj.formatted_text()


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = AddIngredientSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def validate(self, data):

        if self.context['request'].method == 'POST':
            name = data.get('name')
            author = self.context['request'].user
            if Recipe.objects.filter(name=name, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже создали рецепт с таким названием!',
                )

        ingredients = data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients': 'Рецепт нельзя создать без ингредиентов!'},
            )
        names = []
        for ingredient in ingredients:
            ingredient_obj = ingredient['ingredient']['id']
            ingredient_name = ingredient_obj.name
            names.append(ingredient_name)
        if len(names) != len(set(names)):
            raise serializers.ValidationError(
                {'ingredients': 'Ингредиенты не могут повторяться!'}
            )

        tags = data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Рецепту нужен хотя бы один тег!'}
            )
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                {'tags': 'Теги должны быть уникальными!'}
            )

        return data

    @staticmethod
    def create_ingredients(ingredients, recipe):
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['ingredient']['id'],
                amount=ingredient['amount'])
            for ingredient in ingredients
        ])

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.save()

        self.create_ingredients(
            ingredients,
            recipe
        )
        recipe.tags.set(tags)

        return recipe

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        self.create_ingredients(
            validated_data.pop('ingredients'),
            self.instance
        )
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerializer(
            instance, context={
                'request': self.context.get('request')
            }
        ).data

'''
class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        source='recipe.id'
    )

    class Meta:
        model = Favorite
        fields = (
            'id',
            'user',
            'recipe',
        )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            recipe_id = self.context.get('view').kwargs.get('recipe_id')
            user = self.context['request'].user

        if Recipe.objects.filter(id=recipe_id, user=user).exists():
            raise serializers.ValidationError(
                'Вы уже добавили рецепт в избранное!',
            )
        return data

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance, context={
                'request': self.context.get('request')
            }
        ).data
'''