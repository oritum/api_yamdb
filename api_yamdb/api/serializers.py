from rest_framework import serializers

from reviews.models import User


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объекта класса User."""

    class Meta:
        model = User
        fields = ('username', 'email')
