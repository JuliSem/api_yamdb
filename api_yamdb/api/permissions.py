from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Permission для класса User."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permission для классов: Category, Genre, Title."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Permission для классов: Review, Comments."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return (request.user.is_admin
                or request.user.is_moderator
                or (obj.author == request.user))
