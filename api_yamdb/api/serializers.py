"""Сериализаторы для приложения api."""

from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    ValidationError,
)

from reviews.models import User
from users.constants import (
    EMAIL_MAX_LENGTH,
    USERNAME_MAX_LENGTH,
)
from users.validators import validate_username


class BaseUserSerializer(ModelSerializer):
    """Базовый сериализатор для класса User."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class AdminSerializer(BaseUserSerializer):
    """Сериализатор для пользователя с правами администратора."""


class NotAdminSerializer(BaseUserSerializer):
    """Сериализатор для пользователя без прав администратора."""

    class Meta(BaseUserSerializer.Meta):
        read_only_fields = ('role',)


class SignupSerializer(ModelSerializer):
    """Сериализатор для создания объекта класса User."""

    username = CharField(
        max_length=USERNAME_MAX_LENGTH, validators=(validate_username,)
    )
    email = EmailField(max_length=EMAIL_MAX_LENGTH)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        errors = {}
        if (
            User.objects.filter(username=username)
            .exclude(email=email)
            .exists()
        ):
            errors['username'] = 'username используется другим пользователем.'
        if (
            User.objects.filter(email=email)
            .exclude(username=username)
            .exists()
        ):
            errors['email'] = 'email используется другим пользователем.'

        if errors:
            raise ValidationError(errors)

        return data


class CustomTokenObtainSerializer(ModelSerializer):
    """Сериализатор для получения токена."""

    username = CharField(required=True)
    confirmation_code = CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
