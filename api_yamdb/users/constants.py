"""Константы для приложения users."""

ROLE_CHOICES: tuple[tuple[str, str]] = (
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
)

USERNAME_MAX_LENGTH: int = 150

EMAIL_MAX_LENGTH: int = 254

ROLE_MAX_LENGTH: int = 20

FIRST_NAME_MAX_LENGTH: int = 150

LAST_NAME_MAX_LENGTH: int = 150

CONFIRMATION_CODE_MAX_LENGTH: int = 255
