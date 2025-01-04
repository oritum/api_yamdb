"""Константы для приложения users."""

# Роли пользователей:
ROLE_CHOICES: tuple[tuple[str, str]] = (
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
)

# Максимальные длины полей в модели CustomUser:

USERNAME_MAX_LENGTH: int = 150  # username:

EMAIL_MAX_LENGTH: int = 254  # e-mail:

ROLE_MAX_LENGTH: int = 20  # роль пользователя:

FIRST_NAME_MAX_LENGTH: int = 150  # имя пользователя:

LAST_NAME_MAX_LENGTH: int = 150  # фамилия пользователя:

CONFIRMATION_CODE_MAX_LENGTH: int = 255  # код подтверждения:
