from django.contrib.auth import get_user_model
from django.db import models

from reviews.constants import (
    CATEGORY_NAME_MAX_LENGTH,
    CATEGORY_SLUG_MAX_LENGTH,
    GENRE_NAME_MAX_LENGTH,
    GENRE_SLUG_MAX_LENGTH,
    NAME_PREVIEW_LENGTH,
    TEXT_PREVIEW_LENGTH,
    TITLE_NAME_MAX_LENGTH,
)
from reviews.validators import validate_year

User = get_user_model()


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField('Категория', max_length=CATEGORY_NAME_MAX_LENGTH)
    slug = models.SlugField(
        'Слаг категории',
        max_length=CATEGORY_SLUG_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:NAME_PREVIEW_LENGTH]


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField('Жанр', max_length=GENRE_NAME_MAX_LENGTH)
    slug = models.SlugField(
        'Слаг жанра', max_length=GENRE_SLUG_MAX_LENGTH, unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:NAME_PREVIEW_LENGTH]


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        'Название произведения', max_length=TITLE_NAME_MAX_LENGTH
    )
    year = models.SmallIntegerField(
        'Год выпуска произведения',
        validators=[validate_year],
    )
    description = models.TextField(
        'Описание', blank=True, default='Нет описания'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        help_text='Название жанра',
        related_name='titles',
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='titles',
        help_text='Категория произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:NAME_PREVIEW_LENGTH]


class GenreTitle(models.Model):
    """Промежуточная модель для связи произведений и жанров."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    """Модель для отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = models.IntegerField(
        'Оценка', choices=[(i, i) for i in range(1, 11)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'title',
                    'author',
                ),
                name='one_review',
            )
        ]
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.author}: {self.text[:TEXT_PREVIEW_LENGTH]}'


class Comment(models.Model):
    """Модель для комментариев к отзывам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}: {self.text[:TEXT_PREVIEW_LENGTH]}'
