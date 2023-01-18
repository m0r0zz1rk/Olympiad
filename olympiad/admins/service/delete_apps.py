from users.models import Apps


def DeleteUserApps(id_profile) -> None:
    """Удаление всех заявок пользователя"""
    Apps.objects.filter(contact_person_id=id_profile).delete()
    return None
