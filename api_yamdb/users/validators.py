"""Валидаторы для моделей приложения users."""

from django.core.validators import RegexValidator

username_validator = RegexValidator(
    regex=r'^(?!me$)[\w.@+-]+\Z',
    message=(
        'Имя пользователя может содержать только буквы, цифры и символы '
        '@/./+/-/_ и не может быть "me"'
    ),
)
