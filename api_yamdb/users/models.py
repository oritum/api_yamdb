from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import username_validator


class CustomUser(AbstractUser):
    """Кастомная модель пользователя. Переопределяет встроенную."""

    username = models.CharField(
        'Имя пользователя',
        unique=True,
        max_length=150,
        validators=[username_validator],
        error_messages={
            'unique': 'Поле username не уникально.',
        },
    )
    email = models.EmailField(
        'e-mail',
        unique=True,
        max_length=254,
        error_messages={
            'unique': 'Поле email не уникально.',
        },
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
