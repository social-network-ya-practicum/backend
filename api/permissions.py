from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.id == request.user.id


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user and request.user.is_staff)


class IsAuthorAdminOrReadOnly(BasePermission):
    """
    Авторизованные пользователи могут смотреть и создавать.
    Админ или автор поста может редактировать сообщения.
    """

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (
                    request.user.is_staff
                    or request.user.is_superuser
                    or obj.author == request.user
                ))

    def has_permission(self, request, view):
        return request.user.is_authenticated

