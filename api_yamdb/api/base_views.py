"""Базовые представления для API."""

from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.permissions import IsAdminOrReadOnly, IsModeratorAdminPermission
from api.serializers import CategorySerializer, ReviewSerializer
from reviews.models import Category, Title


class CategoryGenreBaseViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """
    Базовый ViwSet для создания, получения и удаления объектов Category и
    Genre."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class ReviewCommentBaseViewSet(ModelViewSet):
    """
    Базовый ViwSet для создания, получения и удаления объектов Review и
    Comment."""

    serializer_class = ReviewSerializer
    permission_classes = (IsModeratorAdminPermission,)
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
    )

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))
