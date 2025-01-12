"""Сериализаторы для приложения api."""

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    EmailField,
    ModelSerializer,
    SlugRelatedField,
    ValidationError,
)

from api.base_serializers import (
    CategoryGenreBaseSerializer,
    TitleBaseSerializer,
    UserBaseSerializer,
)
from reviews.models import Category, Comment, Genre, Review, User
from users.constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from users.validators import validate_username


class AdminSerializer(UserBaseSerializer):
    """Сериализатор для пользователя с правами администратора."""


class NotAdminSerializer(UserBaseSerializer):
    """Сериализатор для пользователя без прав администратора."""

    class Meta(UserBaseSerializer.Meta):
        read_only_fields = ('role',)


class SignupSerializer(UserBaseSerializer):
    """Сериализатор для создания объекта класса User."""

    username = CharField(
        max_length=USERNAME_MAX_LENGTH, validators=(validate_username,)
    )
    email = EmailField(max_length=EMAIL_MAX_LENGTH)

    class Meta(UserBaseSerializer.Meta):
        fields = (
            'email',
            'username',
        )

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


class CustomTokenObtainSerializer(UserBaseSerializer):
    """Сериализатор для получения токена."""

    username = CharField(required=True)
    confirmation_code = CharField(required=True)

    class Meta(UserBaseSerializer.Meta):
        fields = (
            'username',
            'confirmation_code',
        )

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
    """
    Серилизатор для оценок произведений, проверки валидности оценки
    и единичного отзыва на произведение.
    """

    title = SlugRelatedField(slug_field='name', read_only=True)
    author = SlugRelatedField(
        slug_field='username', default=CurrentUserDefault(), read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
            'title',
        )
        read_only_fields = (
            'id',
            'author',
            'title',
            'pub_date',
        )

    def validate_score(self, value):
        if 0 > value > 10:
            raise ValidationError('Оценка должна быть от 1 до 10')
        return value

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(author=author, title=title_id).exists():
            raise ValidationError(
                'Вы уже написали отзыв к этому произведению.'
            )
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('title', None)
        return representation


class CommentSerializer(ModelSerializer):
    """Серилизатор для комментариев на отзыв."""

    review = SlugRelatedField(slug_field='text', read_only=True)
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
            'review',
        )
        read_only_fields = (
            'id',
            'author',
            'review',
            'pub_date',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('review', None)
        return representation


class CategorySerializer(CategoryGenreBaseSerializer):
    """Сериализатор для категорий произведений."""

    class Meta(CategoryGenreBaseSerializer.Meta):
        model = Category


class GenreSerializer(CategoryGenreBaseSerializer):
    """Сериализатор для жанров произведений."""

    class Meta(CategoryGenreBaseSerializer.Meta):
        model = Genre


class TitleReadSerializer(TitleBaseSerializer):
    """Сериализатор для чтения произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta(TitleBaseSerializer.Meta):
        pass


class TitleCreateUpdateDeleteSerializer(TitleBaseSerializer):
    """Сериализатор для создания, изменения и удаления произведений."""

    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta(TitleBaseSerializer.Meta):
        pass

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['genre'] = GenreSerializer(
            instance.genre, many=True
        ).data
        return representation

    def validate_year(self, value):
        if value > timezone.now().year:
            raise ValidationError(
                'Нельзя добавлять произведения, которые ' 'еще не вышли'
            )
        return value

    def validate_genre(self, value):
        if not value:
            raise ValidationError('Поле genre не может быть пустым.')
        return value
