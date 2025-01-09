import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from reviews.models import User,Category, Genre, Title, Review, Comment


MODEL_FILES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comment.csv'
}


class Command(BaseCommand):
    """Management-команда для импорта данных в БД из CSV-файлов."""

    def handle(self, *args, **options):
        """Обработчик импорта данных."""

        for model, file in MODEL_FILES.items():
            with open(
                    f'{settings.CSV_FILES_DIR}/{file}',
                    'r',
                    encoding='utf-8'
            ) as csv_file:
                filedata = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    [model(**data) for data in filedata],
                    ignore_conflicts=True
                )
        self.stdout.write(self.style.SUCCESS('Данные из файла успешно '
                                             'загружены в БД'))
