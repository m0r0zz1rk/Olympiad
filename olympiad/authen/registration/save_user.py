from django.contrib.auth.models import User


def SaveNewUser(login, passw, email):
    """Создание нового пользователя Django"""
    try:
        new = User.objects.create_user(
            username=login,
            password=passw,
            email=email
        )
        return new.id
    except BaseException:
        return False
