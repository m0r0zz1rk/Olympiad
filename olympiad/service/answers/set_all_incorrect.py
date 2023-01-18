from service.models import ChoicesAnswers


def SetAllIncorrect(question_id) -> None:
    """Установить все варианта ответа полученного вопроса неправильными"""
    for choice in ChoicesAnswers.objects.filter(question_id=question_id):
        choice.correct = False
        choice.save()
    return None