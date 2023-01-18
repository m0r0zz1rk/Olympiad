from django.contrib.auth.models import User


def ChangeUserPassword(user_id, passw) -> None:
    """Изменение пароля пользователя"""
    user = User.objects.get(id=user_id)
    user.set_password(passw)
    user.save()
    return None