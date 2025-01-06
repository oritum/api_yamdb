"""Пермишены для API."""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOnlyPermission(BasePermission):
    """Пермишен, предоставляющий доступ только для администраторов."""

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.is_admin


class IsAuthorOrReadOnly(BasePermission):
    """
    Доступ для автора удялять, изменять свои отзывы и комментарии,
    чтение всем.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)


class IsModeratorAdminPermission(BasePermission):
    """
    Доступ для админа и модератора удялять, изменять
    любые отзывы и комментарии.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_moderator
            or request.user.is_admin
        )
