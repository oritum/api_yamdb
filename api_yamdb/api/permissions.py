"""Пермишены для API."""

from rest_framework.permissions import BasePermission


class AdminOnlyPermission(BasePermission):
    """Пермишен для админов."""

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.admin
