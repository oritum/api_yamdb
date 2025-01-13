"""Константы для приложения users."""

ROLE_USER: str = 'user'
ROLE_MODERATOR: str = 'moderator'
ROLE_ADMIN: str = 'admin'

ROLE_CHOICES: tuple[tuple[str, str]] = (
    (ROLE_USER, 'User'),
    (ROLE_MODERATOR, 'Moderator'),
    (ROLE_ADMIN, 'Admin'),
)

USERNAME_MAX_LENGTH: int = 150

EMAIL_MAX_LENGTH: int = 254

ROLE_MAX_LENGTH: int = max(len(role[0]) for role in ROLE_CHOICES)

FIRST_NAME_MAX_LENGTH: int = 150

LAST_NAME_MAX_LENGTH: int = 150

CONFIRMATION_CODE_MAX_LENGTH: int = 255
