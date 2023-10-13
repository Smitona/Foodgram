# Generated by Django 4.2.4 on 2023-10-13 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_cart_options_alter_favorite_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'default_related_name': 'in_%(class)s', 'verbose_name': 'Рецепт в корзине', 'verbose_name_plural': 'Рецепты в корзине'},
        ),
        migrations.AlterModelOptions(
            name='favorite',
            options={'default_related_name': 'in_%(class)s', 'verbose_name': 'Рецепт в избранном', 'verbose_name_plural': 'Рецепты в избранном'},
        ),
    ]
