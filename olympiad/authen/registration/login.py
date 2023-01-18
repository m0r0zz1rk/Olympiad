from random import randrange

from django.contrib.auth.models import User
from pytils import translit


def CreateUserLogin(surname, name) -> str:
    """Генерация логина пользовтеля на основе имени и фамилии"""
    login = f'{translit.slugify(name[:1])}.{translit.slugify(surname)}'
    if User.objects.filter(username=login).exists():
        uniq = False
        new_login = ''
        while uniq is False:
            new_login = f'{login}_{str(randrange(100))}'
            if not User.objects.filter(username=new_login).exists():
                uniq = True
        return new_login
    else:
        return login
