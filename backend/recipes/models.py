from colorfield.fields import ColorField
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from users.models import CustomUser


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=200,
        blank=False,
    )
    measurement_unit = models.CharField(
        blank=False,
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        unique=True,
        blank=False,
        max_length=200,
        verbose_name='Название',
    )
    color = ColorField(
        unique=True,
        blank=False,
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

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    tags = models.ManyToManyField(
        Tag,
        blank=False,
        through='RecipeTag',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        through='RecipeIngredient',
        related_name='ingr_in_recipe'
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
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name[:30]

    def formatted_text(self):
        return '<br>'.join(self.text.splitlines())


class RecipeTag(models.Model):
    """Связанная модель для тегов и рецептов."""

    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,

    )

    class Meta:
        verbose_name = 'Тег для рецепта'
        verbose_name_plural = 'Теги для рецептов'
        ordering = ('recipe',)
        default_related_name = 'tag_for_recipe'

    def __str__(self):
        return 'Тег {} добавлен к рецепту {}.'.format(
            self.tag.name, self.recipe.name[:20]
        )


class RecipeIngredient(models.Model):
    """Связанная модель для ингредиентов и рецептов."""

    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        ordering = ('recipe',)
        default_related_name = 'recipe_ingredients'

    def __str__(self):
        return 'Ингредиент {} добавлен в рецепт {}.'.format(
            self.ingredient.name[:20], self.recipe.name[:20]
        )


class Fields(models.Model):
    """Родительская модель для избранного и корзины."""

    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class Favorite(Fields):
    """Модель избранного."""

    class Meta:
        verbose_name = 'Рецепт в избранном'
        verbose_name_plural = 'Рецепты в избранном'
        default_related_name = 'in_%(class)s'
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
    """Модель корзины."""

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
        default_related_name = 'in_%(class)s'
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
