from rest_framework.generics import get_object_or_404

from users.models import Profiles


def GetFIOLoginedUser(user_id) -> str:
    """Получение ФИО залогиневшегося пользователя"""
    profile = get_object_or_404(
        queryset=Profiles.objects.all(),
        dj_user_id=user_id
    )
    if profile.patronymic == '':
        return f'{profile.surname} {profile.name[:1]}.'
    else:
        return f'{profile.surname} {profile.name[:1]}.{profile.patronymic[:1]}.'