from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
   # is_subscribed = serializers.SerializerMethodField(read_only=True)

    #def get_is_subscribed(self, obj):
       # return obj.followers.filter(
          #  user=self.context.get('follower'),
           # following=obj.author
      #  )

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            #'is_subscribed',
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
           # 'is_subscribed',
        )


class SubscribeSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    #is_subscribed = UserSerializer(read_only=True)

    def get_recipes(self, obj):
        return obj.recipes.filter(author=obj.author)

    def get_recipes_count(self, obj):
        return self.get_recipes.count()

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data

    class Meta:
        model = CustomUser
        fields = fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            #'is_subscribed',
            'recipes',
            'recipes_count',
        )
