"""Сериализаторы для приложения api."""

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    ValidationError,
    SlugRelatedField,
    ValidationError,
    CurrentUserDefault,
)

from reviews.models import User, Review, Comment
from users.constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
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


class SignupSerializer(BaseUserSerializer):
    """Сериализатор для создания объекта класса User."""

    username = CharField(
        max_length=USERNAME_MAX_LENGTH, validators=(validate_username,)
    )
    email = EmailField(max_length=EMAIL_MAX_LENGTH)

    class Meta(BaseUserSerializer.Meta):
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


class CustomTokenObtainSerializer(BaseUserSerializer):
    """Сериализатор для получения токена."""

    username = CharField(required=True)
    confirmation_code = CharField(required=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            raise ValidationError(
                {'confiration_code': 'неверный confirmation_code'}
            )
        return data


class ReviewSerializer(ModelSerializer):
    """Серилизатор для оценка произведений."""
    title = SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = SlugRelatedField(
        slug_field='username',
        default=CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('author', 'title', 'pub_date')

    def validate_score(self, value):
        if 0 > value > 10:
            raise ValidationError(
                'Оценка должна быть от 1 до 10'
            )
        return value


class CommentSerializer(ModelSerializer):
    """Серилизатор для комментариев на отзыв."""
    review = SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('text', 'author', 'pub_date', 'review')
        read_only_fields = ('author', 'review', 'pub_date')
