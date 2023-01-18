import datetime

from django.core.files.storage import default_storage
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import api_view

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from admins.permissions import IsAdministrator
from config.settings import MEDIA_ROOT
from service.answers.create_table_rows import CreateRowsForQuestion
from service.answers.set_all_incorrect import SetAllIncorrect
from service.levels.delete_questions import DeleteLevelQuestions
from service.models import QuestionLevels, Questions, QuestionColumns, TableAnswers, Answers, ChoicesAnswers, \
    QuestionPossibleValues, Olympiads, OlympiadsLevels, ResultsSessions, ResultsQuestions
from service.results.counting import CountingResults
from service.results.recount_participant import Recount
from service.results.xlsx import DownloadResult
from service.serializers import QuestionLevelsListSerializer, QuestionLevelsSerializer, QuestionsSerializer, \
    QuestionColumnsSerializer, TableAnswersSerializer, AnswersSerializer, ChoicesAnswersSerializer, \
    QuestionPossibleValuesSerializier, AccAnswersSerializer, AccRepesentSerializer, OlympiadsSerializer, \
    OlympiadsLevelsSerializer, OlympiadsLevelsCDSerializer, ResultsOlympiadsSerializer, ResultsCompletesSerializer
from users.models import Apps, Profiles


class LevelsListViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка тем вопросов / конкретной темы вопросов"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        'date_create',
        'level',
    ]
    serializer_class = QuestionLevelsListSerializer

    def get_queryset(self):
        qs = QuestionLevels.objects.all()
        if 'data_create' in self.request.GET:
            qs = qs.filter(date_create=self.request.GET.get('date_create'))
        if 'level' in self.request.GET:
            qs = qs.filter(level__contains=self.request.GET.get('level'))
        return qs


class LevelsCUDViewSet(viewsets.ModelViewSet):
    """Создание/удаление/изменение тем вопросов"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = QuestionLevelsSerializer

    def create(self, request, *args, **kwargs):
        try:
            serialize = self.serializer_class(data=request.data)
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                return Response(
                    {'success': 'Тема вопросов успешно добавлена'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': serialize.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except BaseException:
            return Response(
                {'error': 'Наименование темы должно быть уникальным'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        try:
            level = get_object_or_404(
                queryset=QuestionLevels.objects.all(),
                pk=self.kwargs['pk']
            )
            serialize = self.serializer_class(
                instance=level,
                data=request.data,
                partial=True
            )
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                return Response(
                    {'success': 'Тема вопросов успешно изменена'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': serialize.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except BaseException:
            return Response(
                {'error': 'Наименование темы вопросов должно быть уникальным'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        try:
            level = get_object_or_404(
                queryset=QuestionLevels.objects.all(),
                pk=self.kwargs['pk']
            )
            DeleteLevelQuestions(level.id)
            level.delete()
            return Response(
                {'success': 'Тема вопросов успешно удалена'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'success': 'Произошла ошибка во время удаления темы, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class QuestionsListViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка вопросов/конкретного вопроса"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        'date_create',
        'level',
        'type'
    ]
    serializer_class = QuestionsSerializer

    def get_queryset(self):
        qs = Questions.objects.all()
        if 'date_create' in self.request.GET:
            qs = qs.filter(date_create=self.request.GET.get('date_create'))
        if 'level' in self.request.GET:
            qs = qs.filter(level=self.request.GET.get('level'))
        if 'question' in self.request.GET:
            qs = qs.filter(question__contains=self.request.GET.get('question'))
        if 'type' in self.request.GET:
            qs = qs.filter(type=self.request.GET.get('type'))
        return qs


class QuestionsImagesUploadViewSet(viewsets.ViewSet):
    """Загрузка изображений в вопросах для TinyMCE"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]

    def ImageUpload(self, request):
        try:
            file = request.FILES.get('file')
        except BaseException:
            return Response(
                {'error': 'Ошибка при получении файла. Повторите попытку или выберите другой файл'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            filename = f'{MEDIA_ROOT}/questions_images/{datetime.date.today().strftime("%d.%m.%Y")}/user_{str(request.user.id)}.jpg'
            file_path = default_storage.save(filename, file)
            return Response(
                {'location': f'/media/{file_path}'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при сохранении файла, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class QuestionAddViewSet(viewsets.ModelViewSet):
    """Создание нового вопроса"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = QuestionsSerializer

    def create(self, request, *args, **kwargs):
        additional_data = request.data.copy()
        additional_data['date_create'] = datetime.date.today().strftime('%d.%m.%Y')
        serialize = self.serializer_class(data=additional_data)
        if serialize.is_valid(raise_exception=True):
            new_question = serialize.save()
            return Response(
                {'success': str(new_question.id)},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Произошла ошибка, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class QuestionEditViewSet(viewsets.ModelViewSet):
    """Редактирование существеующего вопроса"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = QuestionsSerializer

    def EditQuestion(self, request, **kwargs):
        try:
            question = get_object_or_404(
                queryset=Questions.objects.all(),
                pk=self.kwargs['pk']
            )
            serialize = self.serializer_class(
                instance=question,
                data=request.data,
                partial=True
            )
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                return Response(
                    {'success': 'Вопрос успешно изменен'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Произошла ошибка во время изменения вопроса, повторите попыту позже'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка во время изменения вопроса, повторите попыту позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class QuestionDeleteViewSet(viewsets.ModelViewSet):
    """Удаление вопроса"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]

    def destroy(self, request, *args, **kwargs):
        try:
            question = get_object_or_404(
                queryset=Questions.objects.all(),
                pk=self.kwargs['pk']
            )
            question.delete()
            return Response(
                {'success': 'Вопрос успешно удален'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка во время удаления вопроса, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class QuestionColumnsListViewSet(viewsets.ModelViewSet):
    """Получение списка заголовков таблицы ответов для полученного вопроса"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = QuestionColumnsSerializer

    def get_queryset(self):
        qs = QuestionColumns.objects.all()
        if 'question' in self.request.GET:
            qs = qs.filter(question_id=self.request.GET.get('question'))
        return qs.order_by('seq_number')


class QuestionColumnCDViewSet(viewsets.ModelViewSet):
    """Добавление/удаление заголовков столбцов в таблицах ответов"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = QuestionColumnsSerializer

    def create(self, request, *args, **kwargs):
        if QuestionColumns.objects.filter(question_id=request.data['question']). \
                filter(seq_number=request.data['seq_number']).exists():
            return Response(
                {'error': 'Столбец с таким порядковым номером уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serialize = self.serializer_class(
            data=request.data
        )
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            return Response(
                {'success': 'Заголовок успешно добавлен'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': serialize.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        column = get_object_or_404(
            queryset=QuestionColumns.objects.all(),
            pk=self.kwargs['pk']
        )
        try:
            column.delete()
            return Response(
                {'success': 'Заголовок успешно удален'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TableAnswersListViewSet(viewsets.ModelViewSet):
    """Получение списка ответов на вопрос табличного типа"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = TableAnswersSerializer

    def get_queryset(self):
        qs = TableAnswers.objects.all()
        if 'question' in self.request.GET:
            list_columns = []
            for column in QuestionColumns.objects.filter(question_id=self.request.GET.get('question')):
                list_columns.append(column.id)
            dict_rows = {}
            for rec in qs.filter(column_id__in=list_columns):
                if rec.label not in dict_rows.values():
                    dict_rows[rec.id] = rec.label
            qs = qs.filter(id__in=dict_rows.keys())
        return qs.order_by('seq_number')


class TableAnswersCDViewSet(viewsets.ModelViewSet):
    """Добавление/удаление строк ответов в воросы табличного типа"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = TableAnswersSerializer

    def create(self, request, *args, **kwargs):
        try:
            CreateRowsForQuestion(request.data['label'], request.data['question'], request.data['seq_number'])
            return Response(
                {'success': 'Строка ответов успешно создана'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при создании строки ответов, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        try:
            list_columns = []
            for column in QuestionColumns.objects.filter(question_id=request.data['question_id']):
                list_columns.append(column.id)
            for row in TableAnswers.objects.filter(label=request.data['label']). \
                    filter(column_id__in=list_columns):
                row.delete()
            return Response(
                {'success': 'Строка ответов успешно удалена'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при удалении строки ответов, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TableAnswerViewSet(viewsets.ViewSet):
    """Получение/Изменение правильного ответа по строке ответа и столбцу заголовка вопроса"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = TableAnswersSerializer

    def GetAnswers(self, request):
        try:
            list_columns = []
            for column in QuestionColumns.objects.filter(question_id=request.data['question_id']):
                list_columns.append(column.id)
            dict_answers = {}
            for row in TableAnswers.objects.filter(column_id__in=list_columns):
                dict_answers[f'{row.label}-{row.column_id}'] = row.correct
            return Response(
                {'success': dict_answers},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при получении ответа в строке, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def SetAnswer(self, request):
        try:
            row, _ = TableAnswers.objects.get_or_create(
                label=request.data['label'],
                column_id=request.data['column_id']
            )
            row.correct = request.data['correct']
            row.save()
            return Response(
                {'success': 'Ответ успешно изменен'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'success': 'Произошла ошибка при изменении ответа, повторите попытку позже'},
                status=status.HTTP_200_OK
            )


class ShortAnswerViewSet(viewsets.ModelViewSet):
    """Получение/Изменение подписи/правильного ответа для вопроса с кратким ответом"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = AnswersSerializer

    def GetAnswer(self, request):
        try:
            answer, _ = Answers.objects.get_or_create(
                question_id=request.GET['question_id'],
            )
            ans = get_object_or_404(
                queryset=Answers.objects.all(),
                pk=answer.id
            )
            serialize = self.serializer_class(ans)
            return Response(
                {'success': serialize.data},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при получении ответа, повторите попытку позже'},
                status=status.HTTP_200_OK
            )

    def SetSignature(self, request):
        try:
            answer, _ = Answers.objects.get_or_create(
                question_id=request.data['question_id'],
            )
            answer.label = request.data['label']
            answer.save()
            return Response(
                {'success': 'Подпись к полю ответа успешно изменена'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка во время изменения подписи к полю ответа, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def SetAnswer(self, request):
        try:
            answer, _ = Answers.objects.get_or_create(
                question_id=request.data['question_id'],
            )
            answer.short_correct = request.data['correct']
            answer.save()
            return Response(
                {'success': 'Правильный ответ успешно изменен'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка во время изменения правильного ответа, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ChoiceAnswerViewSet(viewsets.ModelViewSet):
    """Добавление/изменение/удаление вариантов ответов для вопросов классического типа"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = ChoicesAnswersSerializer

    def get_queryset(self):
        return ChoicesAnswers.objects.filter(question_id=self.request.GET.get('question_id'))

    def create(self, request, *args, **kwargs):
        if 'correct' in request.data:
            SetAllIncorrect(request.data['question'])
        serialize = self.serializer_class(data=request.data)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            return Response(
                {'success': 'Вариант ответа успешно добавлен'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Произошла ошибка при добавлении варианта ответа, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        try:
            SetAllIncorrect(request.data['question'])
            choice = get_object_or_404(
                queryset=ChoicesAnswers.objects.all(),
                pk=request.data['choice_id']
            )
            choice.correct = True
            choice.save()
            return Response(
                {'success': 'Правильный ответ успешно изменен'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при изменении правильного ответа, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        try:
            choice = get_object_or_404(
                queryset=ChoicesAnswers.objects.all(),
                pk=self.kwargs['pk']
            )
            choice.delete()
            return Response(
                {'success': 'Вариант ответа успешно удален'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка во время удаления варианта ответа, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class AccordanceChoiceViewSet(viewsets.ModelViewSet):
    """Получение/добавление/удаление вариантов ответа для вопроса типа Соответствие"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = QuestionPossibleValuesSerializier

    def get_queryset(self):
        return QuestionPossibleValues.objects.filter(question_id=self.request.GET.get('question_id'))

    def create(self, request, *args, **kwargs):
        serialize = self.serializer_class(data=request.data)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            return Response(
                {'success': 'Вариант ответа успешно добавлен'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'success': serialize.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        try:
            acc = get_object_or_404(
                queryset=QuestionPossibleValues.objects.all(),
                pk=self.kwargs['pk']
            )
            acc.delete()
            return Response(
                {'success': 'Вариант ответа успешно удален'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'success': 'Произошла ошибка во время удаления варианта ответа, повторите попытку позже'},
                status=status.HTTP_200_OK
            )


class AccReadViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение строк ответов для вопросов типа Соответствие"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = AccRepesentSerializer

    def get_queryset(self):
        return Answers.objects.filter(question_id=self.request.GET.get('question_id'))


class AccAnswersViewSet(viewsets.ModelViewSet):
    """Cоздание/удаление строк ответов для вопросов типа Соответствие"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = AccAnswersSerializer

    def create(self, request, *args, **kwargs):
        serialize = self.serializer_class(data=request.data)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            return Response(
                {'success': 'Строка ответа успешно добавлена'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': serialize.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        try:
            answer = get_object_or_404(
                queryset=Answers.objects.all(),
                pk=self.kwargs['pk']
            )
            answer.delete()
            return Response(
                {'success': 'Строка ответа успешно удалена'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при удалении строки ответа, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class OlympiadsListViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка/объекта олимпиад"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = OlympiadsSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        'event_date',
        'date_reg_start',
    ]

    def get_queryset(self):
        qs = Olympiads.objects.all()
        if 'event_date' in self.request.GET:
            qs = qs.filter(event_date=self.request.GET.get('event_date'))
        if 'theme' in self.request.GET:
            qs = qs.filter(theme__contains=self.request.GET.get('theme'))
        if 'date_reg' in self.request.GET:
            qs = qs.filter(
                date_reg_start__lte=self.request.GET.get('date_reg')
            ).filter(
                date_reg_end__gte=self.request.GET.get('date_reg')
            )
        return qs


class OlympiadsCUDViewSet(viewsets.ModelViewSet):
    """Добавление/изменение/удаление олимпиад"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = OlympiadsSerializer
    queryset = Olympiads.objects.all()

    def create(self, request, *args, **kwargs):
        serialize = self.serializer_class(data=request.data)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            return Response(
                {'success': 'Олимпиада успешно добавлена'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': serialize.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        try:
            olympiad = get_object_or_404(
                queryset=self.queryset,
                pk=self.kwargs['pk']
            )
            serialize = self.serializer_class(
                instance=olympiad,
                data=request.data,
                partial=True
            )
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                return Response(
                    {'success': 'Информация об олимпиаде успешно обновлена'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': serialize.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при обновлении информации об олимпиаде, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        try:
            olympiad = get_object_or_404(
                queryset=self.queryset,
                pk=self.kwargs['pk']
            )
            olympiad.delete()
            return Response(
                {'success': 'Олимпиада успешно удалена'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка во время удаления олимпиады, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class OlympiadsLevelsListViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение распределений тем вопросов на олимпиадах"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = OlympiadsLevelsSerializer

    def get_queryset(self):
        qs = OlympiadsLevels.objects.all()
        if 'olympiad_id' in self.request.GET:
            qs = qs.filter(olympiad_id=self.request.GET.get('olympiad_id'))
        return qs.order_by('seq_number')


class OlympiadLevelsCDViewSet(viewsets.ModelViewSet):
    """Добавление/удаление темы вопросов олимпиады"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = OlympiadsLevelsCDSerializer

    def create(self, request, *args, **kwargs):
        serialize = self.serializer_class(data=request.data)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            return Response(
                {'success': 'Тема вопросов успешно добавлена'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': serialize.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        try:
            level = get_object_or_404(
                queryset=OlympiadsLevels.objects.all(),
                pk=self.kwargs['pk']
            )
            level.delete()
            return Response(
                {'success': 'Тема вопросов успешно удалена'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка во время удаления темы, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ResultsOlympiadsListViewSet(viewsets.ModelViewSet):
    """Получение списка олимпиад с данными об участниках/средним баллом для страницы результатов"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = ResultsOlympiadsSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['event_date']

    def get_queryset(self):
        qs = Olympiads.objects.all().order_by('-event_date')
        if 'theme' in self.request.GET:
            qs = qs.filter(theme__contains=self.request.GET.get('theme'))
        if 'event_date' in self.request.GET:
            qs = qs.filter(date_event=self.request.GET.get('event_date'))
        if any(x in self.request.GET for x in ['participant_surname', 'participant_name', 'participant_id']):
            list_dates = []
            if 'participant_surname' in self.request.GET:
                for app in Apps.objects.filter(surname__contains=self.request.GET.get('participant_surname')):
                    list_dates.append(app.date_create)
            if 'participant_name' in self.request.GET:
                for app in Apps.objects.filter(name__contains=self.request.GET.get('participant_name')):
                    if app.date_create not in list_dates:
                        list_dates.append(app.date_create)
            if 'participant_id' in self.request.GET:
                for app in Apps.objects.filter(identifier__contains=self.request.GET.get('participant_id')):
                    if app.date_create not in list_dates:
                        list_dates.append(app.date_create)
            list_ids = []
            for date in list_dates:
                for olympic in qs.filter(date_reg_start__lte=date).filter(date_reg_end__gte=date):
                    if olympic.id not in list_ids:
                        list_ids.append(olympic.id)
            qs = qs.filter(id__in=list_ids)
        return qs


@api_view(['get'])
def GetOlympiadTheme(request):
    theme = Olympiads.objects.get(id=request.GET.get('olympiad_id')).theme
    return Response(
        {'success': theme},
        status=status.HTTP_200_OK
    )


class ResultsCompletesListViewSet(viewsets.ModelViewSet):
    """Получение списка участников олимпиады"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    serializer_class = ResultsCompletesSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        'surname',
        'contact_person__oo_fullname'
    ]

    def get_queryset(self):
        olympiad = Olympiads.objects.get(id=self.request.GET.get('olympiad_id'))
        qs = Apps.objects.filter(date_create__gte=olympiad.date_reg_start).\
                filter(date_create__lte=olympiad.date_reg_end)
        if 'surname' in self.request.GET:
            qs = qs.filter(surname__contains=self.request.GET.get('surname'))
        if 'name' in self.request.GET:
            qs = qs.filter(name__contains=self.request.GET.get('name'))
        if 'identifier' in self.request.GET:
            qs = qs.filter(identifier__contains=self.request.GET.get('identifier'))
        if 'oo' in self.request.GET:
            list_contact = []
            for profile in Profiles.objects.filter(oo_fullname__contains=self.request.GET.get('oo')):
                list_contact.append(profile.id)
            qs = qs.filter(contact_person_id__in=list_contact)
        return qs


class ResultsActionsViewSet(viewsets.ViewSet):
    """Подсчет/выгрузка в excel результатов олимпиады"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]

    def CountingResults(self, request, **kwargs):
        CountingResults(self.kwargs['olympiad_id'])
        return Response(
            {'success': 'Результаты олимпиады успешно обновлены'},
            status=status.HTTP_200_OK
        )

    def GetFile(self, request, **kwargs):
        olympiad = get_object_or_404(
            queryset=Olympiads.objects.all(),
            pk=self.kwargs['olympiad_id']
        )
        if ResultsSessions.objects.filter(olympiad_theme=olympiad.theme).exists():
            return DownloadResult(self.kwargs['olympiad_id'])
        else:
            return Response(
                {'error': 'Нет результатов для выбранной олимпиады'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ResultQuestionsListViewSet(viewsets.ViewSet):
    """Получение списка вопросов для учатсника олимпиады"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]

    def GetQuestions(self, request, **kwargs):
        session = get_object_or_404(
            queryset=ResultsSessions.objects.all(),
            participant_identifier=self.kwargs['id']
        )
        questions_dict = {}
        count = 1
        for rec in ResultsQuestions.objects.filter(result_session_id=session.id).values('question_id').distinct():
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


class DetailResultActionsViewSet(viewsets.ViewSet):
    """Функции для отображения/сохранения результатов участника олимпиады"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]

    def GetLastFirstName(self, request, **kwargs):
        app = get_object_or_404(
            queryset=Apps.objects.all(),
            identifier=self.kwargs['id']
        )
        return Response(
            {'success': app.surname+' '+app.name},
            status=status.HTTP_200_OK
        )

    def GetClassicAnswers(self, request, **kwargs):
        try:
            ses = get_object_or_404(
                queryset=ResultsSessions.objects.all(),
                participant_identifier=self.kwargs['id']
            )
            dict_classic = {}
            for answer in ResultsQuestions.objects.filter(result_session_id=ses.id):
                if Questions.objects.get(id=answer.question_id).type == 'Классический':
                    correct = ChoicesAnswers.objects.filter(question_id=answer.question_id).\
                        get(correct=True).choice
                    dict_classic[answer.question_id] = [correct, answer.answer_participant, answer.points]
            return Response(
                dict_classic,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при получении ответов на вопросы типа "Классический"'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def SaveClassicDetailPoints(self, request):
        try:
            ses = get_object_or_404(
                queryset=ResultsSessions.objects.all(),
                participant_identifier=request.data['identifier']
            )
            answer = get_object_or_404(
                queryset=ResultsQuestions.objects.filter(result_session_id=ses.id),
                question_id=request.data['question_id']
            )
            answer.points = int(request.data['points'])
            answer.save()
            return Response(
                {'success': 'Баллы за вопрос успешно изменены'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при сохранении баллов, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def GetAccAnswers(self, request, **kwargs):
        try:
            ses = get_object_or_404(
                queryset=ResultsSessions.objects.all(),
                participant_identifier=self.kwargs['id']
            )
            dict_acc = {}
            for answer in ResultsQuestions.objects.filter(result_session_id=ses.id):
                if Questions.objects.get(id=answer.question_id).type == 'Соответствие':
                    list_acc = []
                    for rec in Answers.objects.filter(question_id=answer.question_id):
                        answer = ResultsQuestions.objects.filter(result_session_id=ses.id).\
                            filter(question_id=answer.question_id).get(answer_id=rec.id)
                        list_acc.extend(
                            [
                                rec.label,
                                rec.acc_correct.value,
                                answer.answer_participant,
                                answer.points,
                                answer.answer_id
                            ]
                        )
                    dict_acc[answer.question_id] = list_acc
            return Response(
                dict_acc,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при получении ответов на вопросы типа "Соответствие"'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def SaveShortAccTablePoints(self, request):
        try:
            ses = get_object_or_404(
                queryset=ResultsSessions.objects.all(),
                participant_identifier=request.data['identifier']
            )
            answer = get_object_or_404(
                queryset=ResultsQuestions.objects.filter(result_session_id=ses.id).\
                        filter(question_id=request.data['question_id']),
                answer_id=request.data['answer_id']
            )
            answer.points = int(request.data['points'])
            answer.save()
            return Response(
                {'success': 'Баллы за вопрос успешно изменены'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при сохранении баллов, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def GetShortAnswers(self, request, **kwargs):
        try:
            ses = get_object_or_404(
                queryset=ResultsSessions.objects.all(),
                participant_identifier=self.kwargs['id']
            )
            dict_short = {}
            for answer in ResultsQuestions.objects.filter(result_session_id=ses.id):
                if Questions.objects.get(id=answer.question_id).type == 'Краткий ответ':
                    correct = Answers.objects.get(question_id=answer.question_id)
                    dict_short[answer.question_id] = [
                        correct.label,
                        correct.short_correct,
                        answer.answer_participant,
                        answer.points,
                        answer.answer_id
                    ]
            return Response(
                dict_short,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при получении ответов на вопросы типа "Краткий ответ"'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def GetDetailedAnswers(self, request, **kwargs):
        try:
            ses = get_object_or_404(
                queryset=ResultsSessions.objects.all(),
                participant_identifier=self.kwargs['id']
            )
            dict_detailed = {}
            for answer in ResultsQuestions.objects.filter(result_session_id=ses.id):
                if Questions.objects.get(id=answer.question_id).type == 'Развернутый ответ':
                    dict_detailed[answer.question_id] = [
                        answer.answer_detail_participant,
                        answer.points
                    ]
            return Response(
                dict_detailed,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при получении ответов на вопросы типа "Развернутый ответ"'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def GetTableAnswers(self, request, **kwargs):
        try:
            ses = get_object_or_404(
                queryset=ResultsSessions.objects.all(),
                participant_identifier=self.kwargs['id']
            )
            dict_tables = {}
            for answer in ResultsQuestions.objects.filter(result_session_id=ses.id):
                if Questions.objects.get(id=answer.question_id).type == 'Табличный':
                    dict_columns = {}
                    for column in QuestionColumns.objects.filter(question_id=answer.question_id):
                        dict_rows = {}
                        for row in TableAnswers.objects.filter(column_id=column.id):
                            ans = ResultsQuestions.objects.filter(result_session_id=ses.id).\
                                    filter(question_id=answer.question_id).\
                                    get(answer_id=row.id)
                            dict_rows[row.label] = [
                                row.correct,
                                ans.answer_participant,
                                ans.points,
                                row.id
                            ]
                        dict_columns[column.column] = dict_rows
                    dict_tables[answer.question_id] = dict_columns
            return Response(
                dict_tables,
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при получении ответов на вопросы типа "Развернутый ответ"'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def RecountParticipantResult(self, request, **kwargs):
        try:
            Recount(self.kwargs['identifier'])
            return Response(
                {'success': 'Итоговый балл участника успешно изменен'},
                status=status.HTTP_200_OK
            )
        except BaseException:
            return Response(
                {'error': 'Произошла ошибка при пересчете результатов, повторите попытку позже'},
                status=status.HTTP_400_BAD_REQUEST
            )
