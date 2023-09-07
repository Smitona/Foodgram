from django.core.validators import RegexValidator
from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    # is_subscribed = serializers.SerializerMethodField(read_only=True)
    # recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
          #  'is_subscribed',
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
        #read_only_fields = (
            #'is_subscribed',
       # )


class SubsctibeSerilizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        filels = fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
           # 'is_subscribed',
            'recipies',
            # 'recipes_count',
        )

