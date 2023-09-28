from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[
            RegexValidator(r'^[\w.@+-]+\Z'),
        ],
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
    )
    last_name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
    )
    password = models.CharField(
        max_length=150,
        blank=False,
        validators=[
            RegexValidator(r'^[\w.@+-]+\Z'),
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
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'author'],
                name='unique_follow',
            )
        ]

    def __str__(self) -> str:
        return '{} подписан на {}'.format(
            self.follower, self.author
        )
