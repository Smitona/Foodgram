from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

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

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.folliwing.filter(user=user).exists()

    def recipes_count(self, obj):
        return obj.author.count()


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


class UserMeSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = UserSerializer.Meta.fields
        read_only_fields = (
            'is_subscribed',
        )


class TokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            'password',
            'email',
        )
