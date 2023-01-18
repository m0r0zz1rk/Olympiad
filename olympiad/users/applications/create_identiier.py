from random import randrange

from users.models import Apps


def CreateIdentifier() -> str:
    """Генерация уникльного идентификатора участника"""
    while True:
        identifier = f'{str(randrange(10000, 99999))}-{str(randrange(10000, 99999))}'
        if not Apps.objects.filter(identifier=identifier).exists():
            break
    return identifier
