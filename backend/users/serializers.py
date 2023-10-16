from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from rest_framework import serializers
from users.models import CustomUser, UserFollower


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return user.followers.filter(
            author=obj
        ).exists()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )


class UserMeSerializer(CustomUserSerializer):
    class Meta:
        model = CustomUser
        fields = CustomUserSerializer.Meta.fields
        read_only_fields = (
            'is_subscribed',
        )


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = UserFollower
        fields = (
            'author',
            'follower'
        )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            author_id = self.context.get('view').kwargs.get('user_id')
            author = get_object_or_404(CustomUser, pk=author_id)

            user = self.context['request'].user

            if user == author:
                raise serializers.ValidationError(
                    'Нельзя подписаться на самого себя!',
                )

            if UserFollower.objects.filter(
                follower=user,
                author=author
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого автора!',
                )

            return data

    def to_representation(self, instance):
        return SubscribeSerializer(
            instance, context={
                'request': self.context.get('request')
            }
        ).data


class SubscribeSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.BooleanField(read_only=True)

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return ShortRecipeSerializer(
            recipes, many=True, context=self.context
        ).data

    def get_recipes_count(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return recipes.count()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
