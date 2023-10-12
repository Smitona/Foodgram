import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='The path to the CSV file'
        )

    def handle(self, *args, **options):
        csv_path = options['path'] or str(
            Path(settings.BASE_DIR) / 'data',
        )

        self.import_csv_data(
            csv_path, 'ingredients.csv',
            self.import_ingredients
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Ingredients imported successfully.'
            )
        )

    def import_csv_data(self, csv_path, filename, import_func):
        file_path = Path(csv_path) / filename
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_data = csv.DictReader(file)
            import_func(csv_data)

    def import_ingredients(self, csv_data):
        ingredients = [Ingredient(
            name=row['name'],
            measurement_unit=row['measurement_unit'],
        ) for row in csv_data
        ]
        Ingredient.objects.bulk_create(ingredients)
