from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import username_validator

ROLE_CHOICES = (
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя. Переопределяет встроенную."""

    username = models.CharField(
        'Имя пользователя',
        unique=True,
        blank=False,
        null=False,
        max_length=150,
        validators=[username_validator],
        error_messages={
            'unique': 'Поле username не уникально.',
        },
    )
    email = models.EmailField(
        'e-mail',
        unique=True,
        blank=False,
        null=False,
        max_length=254,
        error_messages={
            'unique': 'Поле email не уникально.',
        },
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
        null=True,
    )
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
