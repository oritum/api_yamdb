from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Доступ для автора удялять, изменять свои отзывы и комментарии,
    чтение всем.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsModeratorPermission(permissions.BasePermission):
    """
    Доступ для админа и модератора удялять, изменять
    любые отзывы и комментарии.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_moderator
            or request.user.is_admin
        )
