from rest_framework import permissions

from participants.models import Sessions


class IsParticipant(permissions.BasePermission):
    """Проверка на пользователя системы"""

    def has_permission(self, request, view):
        return Sessions.objects.filter(unique_id=request.data['uuid']).exists()
