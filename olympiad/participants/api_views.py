import datetime
import pytz

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from participants.answers.get_acc_answer import GetAccAnswer
from participants.answers.get_table_answer import GetTableAnswerStr, GetIdTableAnswer
from participants.models import Sessions, ParticipantsAnswers
from participants.permissions import IsParticipant
from participants.serializers import ParticipantSerializer, OlypmicSerializer, OlympicQuestionsSerializer, \
    ParticipantAnswerFullSerializer
from participants.start.create_answers import CreateParticipantAnswers
from service.models import Olympiads, Questions, QuestionColumns, TableAnswers, Answers, QuestionPossibleValues, \
    ChoicesAnswers
from users.models import Apps


class ParticipantInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение данных об участнике олимпиады на основе полученного uuid"""
    permission_classes = [IsParticipant]
    serializer_class = ParticipantSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            app = get_object_or_404(
                queryset=Apps.objects.all(),
                identifier=session.participant_id
            )
            serialize = self.serializer_class(
                instance=app,
                partial=True
            )
            return Response(
                serialize.data,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {
                    'error': 'Произошла ошибка во время получения данных участника. Пожалуйста, закройте браузер и войдите в систему снова'},
                status=status.HTTP_400_BAD_REQUEST
            )


class OlympiadInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение данных об олимпиаде на основе полученного uuid"""
    permission_classes = [IsParticipant]
    serializer_class = OlypmicSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            olympiad = get_object_or_404(
                queryset=Olympiads.objects.all(),
                pk=session.olympiad_id
            )
            serialize = self.serializer_class(
                instance=olympiad,
                partial=True
            )
            return Response(
                serialize.data,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {
                    'error': 'Произошла ошибка во время получения информации об олимпиаде. Пожалуйста, закройти браузер и войдите в систему снова'},
                status=status.HTTP_400_BAD_REQUEST
            )


class OlympiadStart(viewsets.ViewSet):
    """Начало прохождения олимпиады"""
    permission_classes = [IsParticipant]

    def OlympiadStart(self, request):
        session = get_object_or_404(
            queryset=Sessions.objects.all(),
            unique_id=request.data['uuid']
        )
        session.time_olympic = datetime.datetime.now()
        session.save()
        if not ParticipantsAnswers.objects.filter(session=session.id).exists():
            CreateParticipantAnswers(session.id)
        return Response(
            {'success': 'ok'},
            status=status.HTTP_200_OK
        )


class ParticipantRemainigTimeViewSet(viewsets.ViewSet):
    """Получение оствашегося времени участника для прохождения олимпиады"""
    permission_classes = [IsParticipant]

    def GetRemainingTime(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            olympiad = get_object_or_404(
                queryset=Olympiads.objects.all(),
                pk=session.olympiad_id
            )
            if session.time_stop == 0:
                time_end = session.time_olympic.replace(tzinfo=pytz.timezone('Asia/Irkutsk')) + \
                           datetime.timedelta(hours=8, minutes=olympiad.time_complete)
                if datetime.datetime.now().replace(tzinfo=pytz.timezone('Asia/Irkutsk')) > \
                        time_end.replace(tzinfo=pytz.timezone('Asia/Irkutsk')):
                    return Response(
                        {'error': 'Время прохождения олимпиады вышло'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                remaining = time_end.replace(tzinfo=pytz.timezone('Asia/Irkutsk')) - \
                                    datetime.datetime.now().replace(tzinfo=pytz.timezone('Asia/Irkutsk'))
                seconds = int(remaining.seconds)
            else:
                seconds = session.time_stop
            return Response(
                {'success': seconds},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка, повторите попытку входа'},
                status=status.HTTP_400_BAD_REQUEST
            )


class OlympiadStop(viewsets.ViewSet):
    """Окончание прохождения олимпиады"""
    permission_classes = [IsParticipant]

    def OlympiadStop(self, request):
        session = get_object_or_404(
            queryset=Sessions.objects.all(),
            unique_id=request.data['uuid']
        )
        session.time_finish = datetime.datetime.now()
        session.save()
        return Response(
            {'success': 'ok'},
            status=status.HTTP_200_OK
        )


class ParticipantQuestionsListViewSet(viewsets.ViewSet):
    """Получение списка вопросов для учатсника олимпиады"""
    permission_classes = [IsParticipant]

    def GetQuestions(self, request):
        questions_dict = {}
        session = get_object_or_404(
            queryset=Sessions.objects.all(),
            unique_id=request.data['uuid']
        )
        count = 1
        for rec in ParticipantsAnswers.objects.filter(session=session.id).order_by('seq_number'). \
                values('question_id').distinct():
            question = Questions.objects.get(id=rec['question_id'])
            questions_dict[count] = [
                rec['question_id'],
                question.level.level,
                question.question,
                question.type
            ]
            count += 1
        return Response(
            questions_dict,
            status=status.HTTP_200_OK
        )


class QuestionInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение темы и формулировки вопроса"""
    permission_classes = [IsParticipant]
    serializer_class = OlympicQuestionsSerializer


class QuestionsListViewSet(viewsets.ViewSet):
    """Получение списка столбцов, строк для вопросов табличного типа,
                 списка возможных вариантов ответа для вопросов типа Соответствие и Классический,
                 название поля для вопроса с кратким вариантом ответа участника олимпиады"""
    permission_classes = [IsParticipant]

    def GetListQuestion(self, type):
        session = get_object_or_404(
            queryset=Sessions.objects.all(),
            unique_id=self.request.data['uuid']
        )
        list_ids = []
        for q in ParticipantsAnswers.objects.filter(session=session.id):
            if Questions.objects.get(id=q.question_id).type == type:
                list_ids.append(q.question_id)
        return list_ids

    def GetColumns(self, request):
        try:
            list_ids = self.GetListQuestion('Табличный')
            columns_dict = {}
            for id in list_ids:
                col = {}
                for column in QuestionColumns.objects.filter(question_id=id).order_by('seq_number'):
                    col[column.id] = column.column
                columns_dict[id] = col
            return Response(
                columns_dict,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при получении столбцов для вопросов табличного типа'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def GetRows(self, request):
        try:
            list_ids = self.GetListQuestion('Табличный')
            rows_dict = {}
            for id in list_ids:
                list_cols = []
                for col in QuestionColumns.objects.filter(question_id=id):
                    list_cols.append(col.id)
                row_dict = {}
                for row in TableAnswers.objects.filter(
                        column_id__in=list_cols
                ).order_by('seq_number'):
                    row_dict[row.seq_number] = row.label
                rows_dict[id] = row_dict
            return Response(
                rows_dict,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при получении строк для вопросов табличного типа'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ParticipantAnswerViewSet(viewsets.ModelViewSet):
    """Получение/сохранение ответов на вопросы от участника олимпиады"""
    permission_classes = [IsParticipant]
    serializer_class = ParticipantAnswerFullSerializer

    def GetTableAnswers(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            list_questions = []
            for row in ParticipantsAnswers.objects.filter(session=session.id):
                if Questions.objects.get(id=row.question_id).type == 'Табличный':
                    if row.question_id not in list_questions:
                        list_questions.append(row.question_id)
            cells_dict = {}
            for id in list_questions:
                dict = {}
                for rec in ParticipantsAnswers.objects.filter(question_id=id):
                    dict[GetTableAnswerStr(rec.answer_id)] = rec.answer
                cells_dict[id] = dict

            return Response(
                cells_dict,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'bad request'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def SaveTableAnswer(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            answer = get_object_or_404(
                queryset=ParticipantsAnswers.objects.filter(
                    session=session.id
                ).filter(
                    question_id=request.data['question_id']
                ),
                answer_id=GetIdTableAnswer(request.data['col_id'], request.data['seq_number'])
            )
            data = {
                'answer': request.data['answer'],
                'time_answer': datetime.datetime.now()
            }
            serialize = self.serializer_class(
                instance=answer,
                data=data,
                partial=True
            )
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                return Response(
                    {'success': 'ok'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': serialize.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except BaseException:
            return Response(
                {'error': serialize.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def TakeSimpleAnswers(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            dict = {}
            for rec in ParticipantsAnswers.objects.filter(
                    session=session.id
            ).filter(
                answer_id=0
            ):
                if rec.answer_detailed == '':
                    dict[rec.question_id] = rec.answer
                else:
                    dict[rec.question_id] = rec.answer_detailed
            return Response(
                dict,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'bad request'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def SaveDetailedAnswer(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            answer = get_object_or_404(
                queryset=ParticipantsAnswers.objects.filter(session=session.id),
                question_id=request.data['question_id']
            )
            data = {
                'answer_detailed': request.data['answer'],
                'time_answer': datetime.datetime.now()
            }
            serialize = self.serializer_class(
                instance=answer,
                data=data,
                partial=True
            )
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                return Response(
                    {'success': 'ok'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': serialize.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except BaseException:
            return Response(
                {'error': serialize.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def TakeShortAnswers(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            list_q = []
            for rec in ParticipantsAnswers.objects.filter(session=session.id):
                if Questions.objects.get(id=rec.question_id).type == 'Краткий ответ':
                    if rec.question_id not in list_q:
                        list_q.append(rec.question_id)
            dict = {}
            for answer in ParticipantsAnswers.objects.filter(session=session.id). \
                    filter(question_id__in=list_q):
                dict[answer.question_id] = [
                    answer.answer_id,
                    Answers.objects.get(id=answer.answer_id).label,
                    answer.answer
                ]
            return Response(
                dict,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'bad request'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def SaveShortAnswer(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            answer = get_object_or_404(
                queryset=ParticipantsAnswers.objects.filter(session=session.id).\
                    filter(question_id=request.data['question_id']),
                answer_id=request.data['answer_id']
            )
            data = {
                'answer': request.data['answer'],
                'time_answer': datetime.datetime.now()
            }
            serialize = self.serializer_class(
                instance=answer,
                data=data,
                partial=True
            )
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                return Response(
                    {'success': 'ok'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': serialize.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except BaseException:
            return Response(
                {'error': serialize.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def TakePossibleValues(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            list_q = []
            for rec in ParticipantsAnswers.objects.filter(session=session.id):
                if Questions.objects.get(id=rec.question_id).type == 'Соответствие':
                    if rec.question_id not in list_q:
                        list_q.append(rec.question_id)
            dict = {}
            for id in list_q:
                list_possibles = ['']
                for val in QuestionPossibleValues.objects.filter(question_id=id):
                    list_possibles.append(val.value)
                dict[id] = list_possibles
            return Response(
                dict,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'bad request'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def TakeAccordanceLabels(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            list_q = []
            for rec in ParticipantsAnswers.objects.filter(session=session.id):
                if Questions.objects.get(id=rec.question_id).type == 'Соответствие':
                    if rec.question_id not in list_q:
                        list_q.append(rec.question_id)
            dict = {}
            for id in list_q:
                list_labels = []
                for acc in Answers.objects.filter(question_id=id):
                    list_labels.append(acc.label)
                dict[id] = list_labels
            return Response(
                dict,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'bad request'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def TakeAccordanceAnswers(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            dict_answers = {}
            for rec in ParticipantsAnswers.objects.filter(session=session.id):
                if Questions.objects.get(id=rec.question_id).type == 'Соответствие':
                    dict_answers[f'{rec.question_id}-{Answers.objects.get(id=rec.answer_id).label}'] = rec.answer
            return Response(
                dict_answers,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'bad request'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def SaveAccordanceAnswer(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            answer = get_object_or_404(
                queryset=ParticipantsAnswers.objects.filter(session=session.id).\
                    filter(question_id=request.data['question_id']),
                answer_id=GetAccAnswer(request.data['question_id'], request.data['label'])
            )
            data = {
                'answer': request.data['answer'],
                'time_answer': datetime.datetime.now()
            }
            serialize = self.serializer_class(
                instance=answer,
                data=data,
                partial=True
            )
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                return Response(
                    {'success': 'ok'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': serialize.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except BaseException:
            return Response(
                {'error': 'bad request'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def TakeChoicesAnswers(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            list_q = []
            for rec in ParticipantsAnswers.objects.filter(session=session.id):
                if Questions.objects.get(id=rec.question_id).type == 'Классический':
                    if rec.question_id not in list_q:
                        list_q.append(rec.question_id)
            dict = {}
            for id in list_q:
                list_choices = []
                for row in ChoicesAnswers.objects.filter(question_id=id):
                    list_choices.append(row.choice)
                dict[id] = list_choices
            return Response(
                dict,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'bad request'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def TakeParticipantChoices(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            dict = {}
            for rec in ParticipantsAnswers.objects.filter(session=session.id):
                if Questions.objects.get(id=rec.question_id).type == 'Классический':
                    dict[rec.question_id] = rec.answer
            return Response(
                dict,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'bad request'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def SaveChoice(self, request):
        try:
            session = get_object_or_404(
                queryset=Sessions.objects.all(),
                unique_id=request.data['uuid']
            )
            answer = get_object_or_404(
                queryset=ParticipantsAnswers.objects.filter(session=session.id),
                question_id=request.data['question_id']
            )
            data = {
                'answer': request.data['answer'],
                'time_answer': datetime.datetime.now()
            }
            serialize = self.serializer_class(
                instance=answer,
                data=data,
                partial=True
            )
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                return Response(
                    {'success': 'ok'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': serialize.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except BaseException:
            return Response(
                {'error': serialize.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
def DetectClosePage(request):
    try:
        session = get_object_or_404(
            queryset=Sessions.objects.all(),
            unique_id=request.data['uuid']
        )
        session.time_stop = request.data['seconds']
        session.save()
        return Response(
            {'success': 'Время успешно зафиксировано'},
            status=status.HTTP_200_OK
        )
    except BaseException:
        return Response(
            {'error': 'Ошибка при фиксации времени'},
            status=status.HTTP_400_BAD_REQUEST
        )