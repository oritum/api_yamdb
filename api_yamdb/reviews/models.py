from django.contrib.auth import get_user_model
from django.db import models

import model_fields_params


User = get_user_model()


class Catregory(models.Model):
    """Модель категории произведения."""

    name = models.CharField(
        verbose_name='Категория',
        max_length=model_fields_params.CATEGORY_NAME_LENGTH
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        max_length=model_fields_params.CATEGORY_SLUG_LENGTH
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField(
        verbose_name='Жанр',
        max_length=model_fields_params.GENRE_NAME_LENGTH
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        max_length=model_fields_params.GENRE_SLUG_LENGTH
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        verbose_name='Название произведения',
        max_length=model_fields_params.TITLE_NAME_LENGTH
    )
    year = models.IntegerField(verbose_name='Год выпуска произведения')
    rating = models.IntegerField(
        verbose_name='Рейтинг произведения',
        null=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        default='Нет описания'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        help_text='Названиек жанра',
        related_name='titles',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Catregory,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='titles',
        help_text='Категория произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Промежуточная модель для связи произведений и жанров."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
