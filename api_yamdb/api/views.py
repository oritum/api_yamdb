from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Review, Title
from .permissions import IsAuthorOrReadOnly, IsModeratorAdminPermission
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Получаем список всех отзывов на произведение."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly, IsModeratorAdminPermission)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(
            Title,
            id=title_id
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(
            Title,
            id=title_id
        )
        serializer.save(author=self.request.user, title_id=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Получаем список всех комментариев на отзыв."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, IsModeratorAdminPermission)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review,
            id=review_id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review,
            id=review_id,
        )
        serializer.save(author=self.request.user, review_id=review)
