from rest_framework import permissions


class IsAuthorAdminOrReadOnly(permissions.BasePermission):
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
