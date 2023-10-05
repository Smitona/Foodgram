from rest_framework import serializers

from recipes.models import Recipe
from users.models import CustomUser, UserFollower


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        return obj.followers.filter(
            follower=self.context.get('user'),
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


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UserMeSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = UserSerializer.Meta.fields
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
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFollower
        fields = (
            'author',
            'follower'
        )
    '''
    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user

        if UserFollower.objects.filter(
            follower=user,
            author=data['author']
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора!'
            )

        if user == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )

        return data
    '''
    def to_representation(self, instance):
        return SubscribeSerializer(
            instance.author, context=self.context
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
