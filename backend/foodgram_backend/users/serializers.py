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
"""
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.folliwing.filter(user=user).exists()

    def recipes_count(self, obj):
        return obj.author.count()
"""


class UserCreateSerializer(serializers.ModelSerializer):
    '''password = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(r'^[\w.@+-]+\Z'),
        ],
    )'''

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )
""""
    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
        """


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

