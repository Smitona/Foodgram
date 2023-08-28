from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        required=True,
        validators=[
            RegexValidator(r'^[\w.@+-]+\z'),
        ],
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        required=True,
    )
    first_name = models.CharField(
        max_length=150,
        unique=True,
        required=True,
    )
    last_name = models.CharField(
        max_length=150,
        unique=True,
        required=True,
    )
    password = models.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(r'^[\w.@+-]+\z'),
        ],
    )
    class Meta:
        ordering = ('username',)

    def __str__(self) -> str:
        return self.username


class UserFollower(models.Model):
    follower = models.ForeignKey(
        CustomUser,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='followers'
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        null=True,
        related_name='following'
    )

    class Meta:
        constrains = [
            models.UniqueConstraint(
                fields=['follower', 'author'],
                name='уникальная подписка',
            )
        ]

    def __str__(self) -> str:
        return f'{self.follower} подписан на {self.author}'
