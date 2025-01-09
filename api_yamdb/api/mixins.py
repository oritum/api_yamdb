from rest_framework import mixins, viewsets, status
from rest_framework.response import Response


class GetPostDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class PreventPutMixin:
    """Миксин для защиты от PUT-запросов."""
    def update(self, request, *args, **kwargs):
        if request.method == "PUT":
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
