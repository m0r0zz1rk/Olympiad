from django.contrib.auth.models import User, Group

from users.models import Profiles


def ChangeUserRole(role, id_profile) -> bool:
    """Изменение роли пользователя"""
    user = User.objects.get(id=Profiles.objects.get(id=id_profile).dj_user_id)
    if role == "Администратор":
        if not user.groups.filter(name="Администраторы").exists():
            Group.objects.get(name="Пользователи").user_set.remove(user)
            Group.objects.get(name="Администраторы").user_set.add(user)
    if role == "Пользователь":
        if not user.groups.filter(name="Пользователи").exists():
            if Group.objects.get(name="Администраторы").user_set.count() > 1:
                Group.objects.get(name="Администраторы").user_set.remove(user)
                Group.objects.get(name="Пользователи").user_set.add(user)
            else:
                return False
    return True
