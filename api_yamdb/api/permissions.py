"""Пермишены для API."""

from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOnlyPermission(BasePermission):
    """Доступ только для администраторов."""

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_admin


class IsModeratorAdminPermission(BasePermission):
    """
    Доступ для админа и модератора удялять, изменять
    любые отзывы и комментарии.
    Автору только свои.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
            or request.user.is_staff
        )


class IsAdminOrReadOnly(BasePermission):
    """Доступ на чтение для всех и изменение только для админа."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_staff)
        )
