from service.models import ResultsSessions, ResultsQuestions


def Recount(identifier) -> None:
    """Пересчет результатов участника олимпиады"""
    ses = ResultsSessions.objects.get(participant_identifier=identifier)
    count = 0
    for answer in ResultsQuestions.objects.filter(result_session_id=ses.id):
        count += answer.points
    ses.total_points = count
    ses.save()
    return None