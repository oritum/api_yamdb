from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import (
    AdminOnlyPermission,
    IsAuthorOrReadOnly,
    IsModeratorAdminPermission,
)
from api.serializers import (
    AdminSerializer,
    CustomTokenObtainSerializer,
    NotAdminSerializer,
    SignupSerializer,
    CommentSerializer,
    ReviewSerializer,
    TitleSerializer,
)
from api.utils import send_confirmation_code
from reviews.models import User, Review, Title


class UsersManagementViewSet(ModelViewSet):
    """
    ViewSet для управления пользователями.
    """

    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (
        IsAuthenticated,
        AdminOnlyPermission,
    )
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
    )

    @action(
        methods=(
            'GET',
            'PATCH',
        ),
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def get_user(self, request):
        serializer_class = (
            AdminSerializer if request.user.is_admin else NotAdminSerializer
        )
        if request.method == 'PATCH':
            serializer = serializer_class(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = serializer_class(request.user)
        return Response(serializer.data)


class SignupView(APIView):
    """View для регистрации пользователя и получения кода подтверждения."""

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        send_confirmation_code(
            user.email, default_token_generator.make_token(user)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainView(APIView):
    """View для получения токена по username и confirmation_code."""

    def post(self, request):
        serializer = CustomTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data.get('username')
        )
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK,
        )


class ReviewViewSet(ModelViewSet):
    """
    ViewSet для получения списка отзывов на произведение,
    создания нового отзыва,
    обновления и удаления существующего отзыва.
    """

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly, IsModeratorAdminPermission)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ModelViewSet):
    """
    ViewSet для получения списка комментариев на отзыв,
    создания нового комментария,
    обновления и удаления существующего комментария.
    """


    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, IsModeratorAdminPermission)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

