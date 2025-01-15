"""Фильтр для произведений."""

from django_filters.filters import Filter
from django_filters.rest_framework.filterset import FilterSet

from reviews.models import Title


class TitleFilterSet(FilterSet):
    """
    Фильтр для произведений по категориям, жанрам, названию и году выпуска.
    """

    category = Filter(field_name='category__slug')
    genre = Filter(field_name='genre__slug')
    name = Filter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = (
            'year',
            'category',
            'genre',
            'name',
        )
