from rest_framework.generics import get_object_or_404

from users.models import Profiles


def GetUsernameByPhone(phone) -> int:
    """Получение ID пользовтеля по номеру телефона"""
    profile = get_object_or_404(
        queryset=Profiles.objects.all(),
        phone=phone
    )
    return profile.dj_user.username