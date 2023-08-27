from django.core.validators import RegexValidator
from rest_framework import serializers

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'auth_token'
        )


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField(
        read_only=True,

    )

    class Meta:
        fields =(
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )