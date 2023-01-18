import random

from participants.models import Sessions, ParticipantsAnswers
from service.models import Olympiads, OlympiadsLevels, Questions, Answers, QuestionColumns, TableAnswers, ChoicesAnswers


def CreateParticipantAnswers(session_id) -> None:
    """Создание записей с вопросоами для ответов участника сессии"""
    session = Sessions.objects.get(id=session_id)
    olympiad = Olympiads.objects.get(id=session.olympiad_id)
    levels = OlympiadsLevels.objects.filter(olympiad_id=olympiad.id).order_by('seq_number')
    for level in levels:
        list_ids = []
        questions = Questions.objects.filter(level_id=level.level_id)
        for question in questions:
            list_ids.append(question.id)
        print(list_ids)
        question = Questions.objects.get(id=random.choice(list_ids))
        if question.type in ['Развернутый ответ', 'Классический']:
            new_answer = ParticipantsAnswers(
                session=session_id,
                seq_number=level.seq_number,
                question_id=question.id,
                answer_id=0
            )
            new_answer.save()
        else:
            if question.type in ['Краткий ответ', 'Соответствие']:
                answers = Answers.objects.filter(question_id=question.id)
            elif question.type == 'Табличный':
                list_cols = []
                columns = QuestionColumns.objects.filter(question_id=question.id)
                for column in columns:
                    list_cols.append(column.id)
                answers = TableAnswers.objects.filter(column_id__in=list_cols)
            else:
                answers = ChoicesAnswers.objects.filter(question_id=question.id)
            for answer in answers:
                new_answer = ParticipantsAnswers(
                    session=session_id,
                    seq_number=level.seq_number,
                    question_id=question.id,
                    answer_id=answer.id
                )
                new_answer.save()
    return None