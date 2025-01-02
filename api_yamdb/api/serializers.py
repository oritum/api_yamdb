from rest_framework.serializers import ModelSerializer, CharField, ValidationError

from reviews.models import User


class UsersSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'username', 'role', 'bio', 'first_name', 'last_name',
        )


class NotAdminSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'username', 'role', 'bio', 'first_name', 'last_name',
        )


class SignupSerializer(ModelSerializer):
    """Сериализатор для создания объекта класса User."""

    class Meta:
        model = User
        fields = ('email', 'username')


class CustomTokenObtainSerializer(ModelSerializer):
    """Сериализатор для получения токена."""
    username = CharField(required=True)
    confirmation_code = CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
