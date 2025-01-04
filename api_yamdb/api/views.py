from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import AdminOnlyPermission
from api.serializers import (
    AdminSerializer,
    CustomTokenObtainSerializer,
    NotAdminSerializer,
    SignupSerializer,
)
from api.utils import send_confirmation_code
from reviews.models import User


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

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(
                {'error': 'метод PUT не разрешён'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().update(request, *args, **kwargs)


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
        if not default_token_generator.check_token(
            user, serializer.validated_data.get('confirmation_code')
        ):
            return Response(
                {'confirmation_code': 'неверный confirmation_code'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK,
        )
