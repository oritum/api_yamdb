"""Утилиты для проекта api_yamdb."""

import random
import string

from django.conf import settings
from django.core.mail import EmailMessage


def generate_confirmation_code(length=6):
    """Генерация кода подтверждения."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def send_confirmation_code(email, confirmation_code):
    """Отправка кода подтверждения по email."""
    EmailMessage(
        subject='Код подтверждения',
        body=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    ).send(fail_silently=False)
