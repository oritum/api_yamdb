"""Утилиты для проекта api_yamdb."""

from django.conf import settings
from django.core.mail import EmailMessage


def send_confirmation_code(email, confirmation_code):
    """Отправка кода подтверждения по email."""

    EmailMessage(
        subject='Код подтверждения',
        body=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    ).send(fail_silently=False)
