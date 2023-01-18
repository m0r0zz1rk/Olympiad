from rest_framework import permissions


class IsUser(permissions.BasePermission):
    """Проверка на пользователя системы"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Пользователи').exists()
