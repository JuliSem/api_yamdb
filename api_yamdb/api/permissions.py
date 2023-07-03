from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Permission для класса User."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permission для классов: Category, Genre, Title."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_admin
                         or request.user.is_superuser)))


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Permission для классов: Review, Comments."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_admin
                or request.user.is_moderator
                or (obj.author == request.user))
