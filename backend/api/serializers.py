from drf_extra_fields.fields import Base64ImageField

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import Recipe, Ingredient, Tag, RecipeIngredient
from users.serializers import UserSerializer


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
    author = UserSerializer(read_only=True)
    text = serializers.SerializerMethodField()
    # is_favorited = serializers.BooleanField(read_only=True)
    # is_in_shopping_cart = serializers.BooleanField(read_only=True)

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
            # 'is_favorited',
            # 'is_in_shopping_cart',
        )

    @staticmethod
    def get_text(obj):
        return obj.formatted_text()

    """ def get_is_favorited(self):
        pass """
    """ def get_is_in_shopping_cart(self):"""


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
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
    '''
    def validate(self, data):
        if self.context['request'].method == 'POST':
            recipe_id = self.context.get('view').kwargs.get('recipe_id')
            recipe = get_object_or_404(Recipe, pk=recipe_id)
            author = self.context['request'].user

        if Recipe.objects.filter(id=recipe_id, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже создали рецепт с таким названием!',
            )
        return data
    '''
    @staticmethod
    def create_ingredients(ingredients, recipe):
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['ingredient']['id'],
                amount=ingredient['amount'])
            for ingredient in ingredients
        ])

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
            recipe = get_object_or_404(Recipe, pk=recipe_id)
            user = self.context['request'].user

        if Recipe.objects.filter(name=recipe, user=user).exists():
            raise serializers.ValidationError(
                'Вы уже добавили рецепт в избранное!',
            )
        return data
    
    def to_representation(self, instance):
        return Seralizer(
            instance, context={
                'request': self.context.get('request')
            }
        ).data
'''