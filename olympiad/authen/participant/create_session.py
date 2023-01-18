import random
import uuid

from participants.models import Sessions


def CreateParticipantSession(participant_id, olympiad_id) -> object:
    """Создание сессии участника олимпиады"""
    while True:
        participant_uuid = uuid.uuid1(random.randint(0, 281474976710655))
        if not Sessions.objects.filter(unique_id=participant_uuid).exists():
            break
    session = Sessions(
        participant_id=participant_id,
        unique_id=participant_uuid,
        olympiad_id=olympiad_id
    )
    session.save()
    return session