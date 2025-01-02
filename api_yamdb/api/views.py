from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import AdminOnlyPermission
from api.serializers import (
    CustomTokenObtainSerializer,
    NotAdminSerializer,
    SignupSerializer,
    UsersSerializer,
)
from api.utils import generate_confirmation_code, send_confirmation_code
from reviews.models import User


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (
        IsAuthenticated,
        # AdminOnlyPermission,
    )
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def get_current_user_info(self, request):
        if request.method == 'PATCH':
            serializer_class = (
                UsersSerializer
                if request.user.is_admin
                else NotAdminSerializer
            )
            serializer = serializer_class(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UsersSerializer(request.user)
        return Response(serializer.data)


class SignupView(APIView):
    """View для создания пользователя и отправки кода подтверждения."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = generate_confirmation_code()
        user.confirmation_code = confirmation_code
        user.save()
        send_confirmation_code(
            email=user.email, confirmation_code=confirmation_code
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainView(APIView):
    """View для получения токена."""

    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if not username or not confirmation_code:
            return Response(
                {'error': 'не указан username или confirmation_code'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )
        if user.confirmation_code != confirmation_code:
            return Response(
                {'error': 'Неверный confirmation_code'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {'refresh': str(refresh), 'access': str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )
