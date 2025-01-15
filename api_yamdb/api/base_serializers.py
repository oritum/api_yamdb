"""Базовые сериализоаторы для API."""

from rest_framework.serializers import IntegerField, ModelSerializer

from reviews.models import Title, User


class UserBaseSerializer(ModelSerializer):
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


class CategoryGenreBaseSerializer(ModelSerializer):
    """Базовый сериализатор для классов Category и Genre."""

    class Meta:
        lookup_field = 'slug'
        fields = (
            'name',
            'slug',
        )


class TitleBaseSerializer(ModelSerializer):
    """Базовый сериализатор для класса Title."""

    rating = IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
