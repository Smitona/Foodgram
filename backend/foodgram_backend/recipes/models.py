from django.db import models
from django.core.validators import RegexValidator

from users.models import CustomUser


class Ingredients(models.Model):
    KILO = 'KILOGRAMMS'
    GRAMMS = 'GRAMMS'
    POINTS = 'POINTS'
    LITRS = 'LITRS'
    ML = 'MILILITRS'
    T_SP = 'TABLE-SPOONS'
    SP = 'SPOONS'
    GL = 'GLASS'
    EYE = 'BY EYE'
    UNITS = [
        (KILO, 'кг'),
        (GRAMMS, 'г'),
        (POINTS, 'шт'),
        (LITRS, 'л'),
        (ML, 'мл'),
        (T_SP, 'ложка'),
        (SP, 'чайная ложка'),
        (GL, 'стакан')
        (EYE, 'на глаз')
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
    tags = models.IntegerChoices(requiered=True,)
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipies',
    )
    ingredients = models.OneToManyField(Ingredients, required=True,)
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
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (в минутах)',
        required=True,
    )
