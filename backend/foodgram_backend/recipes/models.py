from django.db import models
from django.core.validators import (
    RegexValidator, MaxValueValidator, MinValueValidator
)

from users.models import CustomUser


class Ingredient(models.Model):
    KILO = 'KILOGRAMMS'
    GRAMMS = 'GRAMMS'
    POINTS = 'POINTS'
    ML = 'MILILITRS'
    LT = 'LITRS'
    T_SP = 'TABLE-SPOONS'
    SP = 'SPOONS'
    GL = 'GLASS'
    EYE = 'BY EYE'
    DROP = 'DROP'
    SACHET = 'SACHET'
    PIECE = 'PIECE'
    TUFT = 'TUFT'
    PINCH = 'PINCH'
    SLICE = 'SLICE'
    CAN = 'CAN'
    PACKAGE = 'PACKAGE'
    CLOVE = 'CLOVE'
    HANDFUL = 'HANDFUL'
    PACK = 'PACK'
    STICK = 'STICK'
    BOTTLE = 'BOTTLE'
    LOAF = 'LOAF'
    LEAF = 'LEAF'
    SCAPE = 'SCAPE'
    LIKING = 'LIKING'
    STAR = 'STAR'
    LAYER = 'LAYER'
    LT_SACHET = 'LITTLE_SACHET'
    BIRD = 'BIRD'
    UNITS = [
        (KILO, 'кг'),
        (GRAMMS, 'г'),
        (POINTS, 'шт.'),
        (ML, 'мл'),
        (LT, 'л'),
        (T_SP, 'ст. л.'),
        (SP, 'ч. л.'),
        (GL, 'стакан'),
        (EYE, 'на глаз'),
        (DROP, 'капля'),
        (SACHET, 'пакет'),
        (PIECE, 'кусок'),
        (TUFT, 'пучок'),
        (PINCH, 'щепотка'),
        (SLICE, 'долька'),
        (CAN, 'банка'),
        (PACKAGE, 'упаковка'),
        (CLOVE, 'зубчик'),
        (HANDFUL, 'горсть'),
        (PACK, 'пачка'),
        (STICK, 'веточка'),
        (BOTTLE, 'бутылка'),
        (LOAF, 'батон'),
        (LEAF, 'лист'),
        (SCAPE, 'стебель'),
        (LIKING, 'по вкусу'),
        (STAR, 'звездочка'),
        (LAYER, 'пласт'),
        (BIRD, 'тушка'),
        (LT_SACHET, 'пакетик'),
    ]

    name = models.CharField(
        max_length=200,
        required=True,
    )
    measurement_unit = models.CharField(
        required=True,
        choices=UNITS,
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

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        requiered=True,
        through='RecipeTags',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipies',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        required=True,
        through='RecipeIngredients',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        required=True,
    )
    image = models.ImageField(
        required=True,
        verbose_name='Ссылка на картинку на сайте',
    )
    text = models.TextField(
        verbose_name='Описание',
        required=True,
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        required=True,
        default=15,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )


class RecipeTags(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class RecipeIngredients(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
