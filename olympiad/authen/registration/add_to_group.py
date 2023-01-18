from django.contrib.auth.models import User, Group


def AddUserToGroup(user_id) -> None:
    """Добавление пользователя в группу (если пользователь первый, то создаются две новые группы:
       Администраторы и Пользователи, а сам пользователь добавляется в группу Администраторы)"""
    if User.objects.all().count() == 1:
        admins = Group.objects.create(name='Администраторы')
        Group.objects.create(name='Пользователи')
        admins.user_set.add(User.objects.get(id=user_id))
        return None
    else:
        users = Group.objects.get(name='Пользователи')
        users.user_set.add(User.objects.get(id=user_id))
        return None