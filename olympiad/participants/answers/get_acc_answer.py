from service.models import Answers


def GetAccAnswer(question_id, label):
    return Answers.objects.filter(question_id=question_id).\
            filter(label=label).latest('id').id