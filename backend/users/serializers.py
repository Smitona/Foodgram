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


class SubscribeSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    author = UserSerializer(read_only=True)

    def get_recipes(self, obj):
        return Recipe.objects.filter(author=obj)

    def get_recipes_count(self, obj):
        return self.get_recipes.count()

    class Meta:
        model = UserFollower
        fields = (
            'author',
            'recipes',
            'recipes_count',
        )


class SubscribeListSerializer(SubscribeSerializer):

    class Meta:
        model = UserFollower
        fields = SubscribeSerializer.Meta.fields
        read_only_fields = '__all__'