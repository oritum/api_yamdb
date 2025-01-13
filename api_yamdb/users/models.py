from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import (
    EMAIL_MAX_LENGTH,
    FIRST_NAME_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
    ROLE_ADMIN,
    ROLE_CHOICES,
    ROLE_MAX_LENGTH,
    ROLE_MODERATOR,
    USERNAME_MAX_LENGTH,
)
from users.validators import validate_username


class CustomUser(AbstractUser):
    """Кастомная модель пользователя. Переопределяет встроенную."""

    username = models.CharField(
        'Имя пользователя',
        unique=True,
        null=False,
        max_length=USERNAME_MAX_LENGTH,
        validators=[validate_username],
    )
    email = models.EmailField(
        'e-mail',
        unique=True,
        null=False,
        max_length=EMAIL_MAX_LENGTH,
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=ROLE_MAX_LENGTH,
        choices=ROLE_CHOICES,
        default='user',
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        default='',
    )
    first_name = models.CharField(
        'Имя',
        max_length=FIRST_NAME_MAX_LENGTH,
        blank=True,
        default='',
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=LAST_NAME_MAX_LENGTH,
        blank=True,
        default='',
    )

    @property
    def is_moderator(self):
        return self.role == ROLE_MODERATOR

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
