import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import Recipe, Ingredient, Tag, RecipeIngredients, UNITS


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)


class IngridientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.ChoiceField(choices='UNITS')

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'amount',
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


class RecipeCreateSeralizer(serializers.ModelSerializer):
    ingredients = IngridientSerializer(read_only=True, many=True)
    tags = serializers.ChoiceField(many=True, choices='recipies')
    image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        Model = Recipe
        fields = (
            'id',
            'tags',
            'author'
            'ingridients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

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

    def create(self, validated_data):
        ingridients = validated_data.pop('ingridients')
        recipe = Recipe.objects.create(**validated_data)

        for ingridient in ingridients:
            current_ingridient, status = Ingredient.objects.get_or_create(
                **ingridient
            )
            RecipeIngredients.objects.create(
                ingridient=current_ingridient, recipe=recipe
            )
        return recipe


class RecipeSeralizer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    image = RecipeCreateSeralizer(required=True, allow_null=False)
    ingredients = RecipeCreateSeralizer(read_only=True, many=True)
    tags = serializers.ChoiceField(many=True, choices='recipies')
    # is_favorited = serializers.
    is_in_shopping_cart = serializers.SerializerMethodField

    class Meta:
        Model = Recipe
        fields = (
            'id',
            'tags',
            'author'
            'ingridients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    """     def get_is_favorited(self):
        pass """
    """ def get_is_in_shopping_cart(self):"""



