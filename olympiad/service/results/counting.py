from participants.models import Sessions, ParticipantsAnswers
from service.models import ResultsSessions, Olympiads, ResultsQuestions, Questions, ChoicesAnswers, Answers, \
    TableAnswers
from users.models import Apps, Profiles


def CountingResults(olympiad_id) -> None:
    """Подсчет результатов олимпиады"""
    if Sessions.objects.filter(olympiad_id=olympiad_id).exists():
        list_sessions = []
        for session in Sessions.objects.filter(olympiad_id=olympiad_id):
            if ParticipantsAnswers.objects.filter(session=session.id).exists():
                list_sessions.append(session.id)
        for id_l in list_sessions:
            ses = Sessions.objects.get(id=id_l)
            olympiad = Olympiads.objects.get(id=ses.olympiad_id)
            participant = Apps.objects.get(identifier=ses.participant_id)
            result_session = ResultsSessions(
                olympiad_theme=olympiad.theme,
                event_date=olympiad.event_date,
                participant_surname=participant.surname,
                participant_name=participant.name,
                participant_identifier=ses.participant_id,
                participant_oo=Profiles.objects.get(id=participant.contact_person_id).oo_fullname,
                participant_start=ses.time_olympic,
                participant_end=ses.time_finish
            )
            result_session.save()
            count = 0
            for answer in ParticipantsAnswers.objects.filter(session=id_l).order_by('seq_number'):
                question = Questions.objects.get(id=answer.question_id)
                res_q = ResultsQuestions(
                    result_session_id=result_session.id,
                    question_theme=question.level.level,
                    question=question.question,
                    question_id=answer.question_id,
                    answer_id=answer.answer_id,
                )
                res_q.save()
                if question.type in ['Классический', 'Краткий ответ', 'Табличный', 'Соответствие']:
                    res_q.answer_participant = answer.answer
                    if question.type == 'Классический':
                        correct_answer = ChoicesAnswers.objects.filter(question_id=question.id).\
                            filter(correct=True).latest('id').choice
                    elif question.type == 'Краткий ответ':
                        correct_answer = Answers.objects.get(id=answer.answer_id).short_correct
                    elif question.type == 'Табличный':
                        correct_answer = TableAnswers.objects.get(id=answer.answer_id).correct
                    else:
                        correct_answer = Answers.objects.get(id=answer.answer_id).acc_correct.value
                    correct_str = correct_answer.lower().strip()
                    participant_str = answer.answer.lower().strip()
                    if correct_str == participant_str:
                        res_q.points = 1
                        count += 1
                    else:
                        res_q.points = 0
                    res_q.save()
                else:
                    res_q.answer_detail_participant = answer.answer_detailed
                    res_q.save()
                answer.delete()
            result_session.total_points = count
            result_session.save()
            ses.delete()
    return None



