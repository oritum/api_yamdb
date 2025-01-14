from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.base_views import CategoryGenreBaseViewSet, ReviewCommentBaseViewSet
from api.filters import TitleFilterSet
from api.permissions import AdminOnlyPermission, IsAdminOrReadOnly
from api.serializers import (
    AdminSerializer,
    CommentSerializer,
    CustomTokenObtainSerializer,
    GenreSerializer,
    NotAdminSerializer,
    SignupSerializer,
    TitleCreateUpdateDeleteSerializer,
    TitleReadSerializer,
)
from api.utils import send_confirmation_code
from reviews.models import Genre, Review, Title, User


class UsersManagementViewSet(ModelViewSet):
    """
    ViewSet для управления пользователями.

    Предоставляет следующие действия:
    - Получение списка всех пользователей
    - Создание нового пользователя
    - Частичное обновление данных пользователя
    - Удаление пользователя
    - Получение или обновление данных текущего пользователя (/users/me/)
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


class ReviewViewSet(ReviewCommentBaseViewSet):
    """
    ViewSet для получения списка отзывов на произведение (доступно для всех),
    создания нового отзыва (доступно только аутентифицированным пользователям),
    обновления и удаления существующего отзыва (доступно только модераторам и
    администраторам).
    PUT-запросы запрещены.
    """

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ReviewCommentBaseViewSet):
    """
    ViewSet для получения списка комментариев на отзыв (доступно для всех),
    создания нового комментария (доступно только аутентифицированным
    пользователям), обновления и удаления существующего комментария (доступно
    только модераторам и администраторам).
    PUT-запросы запрещены.
    """

    serializer_class = CommentSerializer

    def get_review(self):
        title = self.get_title()
        return get_object_or_404(
            Review, id=self.kwargs.get('review_id'), title=title
        )

    def get_queryset(self):
        self.get_title()
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class CategoryViewSet(CategoryGenreBaseViewSet):
    """
    ViewSet для получения списка категорий (доступно для всех) и создания,
    изменения и удаления категории (доступно только админу).
    """


class GenreViewSet(CategoryGenreBaseViewSet):
    """
    ViewSet для получения списка жанров (доступно для всех) и создания,
    изменения и удаления жанра (доступно только админу).
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """
    ViewSet для получения списка произведений (доступно для всех), создания,
    изменения и удаления произведения (доступно только админу).
    """

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete',
    )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleCreateUpdateDeleteSerializer
