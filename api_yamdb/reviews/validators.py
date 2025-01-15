from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Валидатор года выпуска произведения."""

    if value > timezone.now().year:
        raise ValidationError(
            'Нельзя добавлять произведения, которые еще не вышли.'
        )
    return value
