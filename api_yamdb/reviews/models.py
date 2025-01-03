from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from api_yamdb.users.models import CustomUser


class Catregory(models.Model):
    """Модель категории произведения"""

    name = models.CharField(verbose_name='Категория', max_length=50)
    slug = models.SlugField(verbose_name='Слаг категории', max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения"""

    name = models.CharField(verbose_name='Жанр', max_length=50)
    slug = models.SlugField(verbose_name='Слаг жанра', max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения"""

    name = models.CharField(
        verbose_name='Название произведения',
        max_length= 100
    )
    year = models.IntegerField(verbose_name='Год выпуска произведения')
    rating = models.IntegerField(
        verbose_name='Рейтинг произведения',
        null=True
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=300,
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
    """Промежуточная модель для связи произведений и жанров"""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(
        'Текст отзыва',
        max_length=500
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        help_text='Установите оценку произведению от 1 до 10',
        validators=(MinValueValidator(1), MaxValueValidator(10),))

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.text[:50]}...'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(verbose_name='Текст комментария', max_length=500)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.text[:50]}...'
