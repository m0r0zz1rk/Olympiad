from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):
    """Проверка на администратора системы"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Администраторы').exists()
