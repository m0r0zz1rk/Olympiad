from service.models import Questions


def DeleteLevelQuestions(level_id) -> None:
    """Удаление всех вопросов уровня"""
    for question in Questions.objects.filter(level_id=level_id):
        question.delete()
    return None