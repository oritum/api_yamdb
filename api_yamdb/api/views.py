from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin

from api.serializers import SignupSerializer
from reviews.models import User


class SignupViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """View для создания пользователя."""

    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )