from django.db import models
from django.core.validators import (
    RegexValidator, MaxValueValidator, MinValueValidator
)

from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
    )
    measurement_unit = models.CharField(
        blank=False,
        max_length=25,
    )

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет в HEX',
        default='#ffffff',
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Уникальный слаг',
        validators=[
            RegexValidator(r'^[-a-zA-Z0-9_]+$'),
        ],
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        through='RecipeTag',
        related_name='recipes',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        through='RecipeIngredient',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        blank=False,
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=False,
        null=False,
        verbose_name='Ссылка на картинку на сайте',
    )
    text = models.TextField(
        verbose_name='Описание',
        blank=False,
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        blank=False,
        default=15,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    pub_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name[:30]

    def formatted_text(self):
        return '<br>'.join(self.text.splitlines())


class RecipeTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
    )


class Fields(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_%(class)s'
    )

    class Meta:
        abstract = True


class Favorite(Fields):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite',
            )
        ]

    def __str__(self) -> str:
        return 'Рецепт {} в избранном у {} {}.'.format(
            self.recipe.name, self.user.first_name, self.user.last_name
        )


class Cart(Fields):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart_item',
            )
        ]

    def __str__(self) -> str:
        return 'Рецепт {} добавлен в корзину {} {}.'.format(
            self.recipe.name, self.user.first_name, self.user.last_name
        )
