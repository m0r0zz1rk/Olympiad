import pytz
from rest_framework import serializers

from participants.models import Sessions
from service.models import QuestionLevels, Questions, QuestionColumns, TableAnswers, Answers, ChoicesAnswers, \
    QuestionPossibleValues, Olympiads, OlympiadsLevels, ResultsSessions
from users.models import Apps, Profiles


class QuestionLevelsListSerializer(serializers.ModelSerializer):
    """Сериализация модели уровней вопросов для readonly"""
    question_count = serializers.SerializerMethodField()

    def get_question_count(self, obj):
        return Questions.objects.filter(level_id=obj.id).count()

    class Meta:
        model = QuestionLevels
        fields = '__all__'


class QuestionLevelsSerializer(serializers.ModelSerializer):
    """Сериализация модели уровней вопросов"""

    class Meta:
        model = QuestionLevels
        fields = '__all__'


class QuestionsSerializer(serializers.ModelSerializer):
    """Сериализация модели вопросов"""
    level = serializers.SlugRelatedField(slug_field='level', queryset=QuestionLevels.objects.all())

    class Meta:
        model = Questions
        fields = '__all__'


class QuestionColumnsSerializer(serializers.ModelSerializer):
    """Сериализцаия модели заголовков таблиц ответов"""

    class Meta:
        model = QuestionColumns
        fields = '__all__'


class TableAnswersSerializer(serializers.ModelSerializer):
    """Сериализация модели ответов на вопросы табличного типа"""

    class Meta:
        model = TableAnswers
        fields = '__all__'


class AnswersSerializer(serializers.ModelSerializer):
    """Сериализация модели ответов на вопросы типа: краткий ответ"""

    class Meta:
        model = Answers
        exclude = ('acc_correct',)


class QuestionPossibleValuesSerializier(serializers.ModelSerializer):
    """Сериализация возможных вариантов ответа для вопросов типа Соответствие"""

    class Meta:
        model = QuestionPossibleValues
        fields = '__all__'


class AccAnswersSerializer(serializers.ModelSerializer):
    """Сериализация модели ответов на вопросы типа: соответствие"""

    class Meta:
        model = Answers
        exclude = ('short_correct',)


class ValueField(serializers.RelatedField):
    def to_representation(self, value):
        return value.value


class AccRepesentSerializer(serializers.ModelSerializer):
    """Сериализация модели ответов на вопросы типа: соответствие"""
    acc_correct = ValueField(
        read_only=True
    )

    class Meta:
        model = Answers
        exclude = ('short_correct',)


class ChoicesAnswersSerializer(serializers.ModelSerializer):
    """Сериализация модели ответов для вопросов классического типа"""

    class Meta:
        model = ChoicesAnswers
        fields = '__all__'


class OlympiadsSerializer(serializers.ModelSerializer):
    """Сериализация модели олимпиад"""

    class Meta:
        model = Olympiads
        fields = '__all__'


class OlympiadsLevelsSerializer(serializers.ModelSerializer):
    """Сериализация распределений уровней вопросов на олимпиадах"""
    level = serializers.SlugRelatedField(
        slug_field='level',
        queryset=OlympiadsLevels.objects.all()
    )

    class Meta:
        model = OlympiadsLevels
        fields = '__all__'


class OlympiadsLevelsCDSerializer(serializers.ModelSerializer):
    """Сериализация распределений уровней вопросов на олимпиадах"""

    class Meta:
        model = OlympiadsLevels
        fields = '__all__'


class ResultsOlympiadsSerializer(serializers.ModelSerializer):
    """Сериализация данных об олимпиаде и участниках для результатов"""
    total_count = serializers.SerializerMethodField()
    complete_count = serializers.SerializerMethodField()
    avg_points = serializers.SerializerMethodField()

    def get_total_count(self, obj):
        return Apps.objects.filter(date_create__gte=obj.date_reg_start). \
            filter(date_create__lte=obj.date_reg_end).count()

    def get_complete_count(self, obj):
        count = 0
        list_identifier = []
        for app in Apps.objects.filter(date_create__gte=obj.date_reg_start).filter(date_create__lte=obj.date_reg_end):
            list_identifier.append(app.identifier)
        for session in Sessions.objects.filter(participant_id__in=list_identifier):
            if session.time_finish.replace(tzinfo=pytz.timezone('Asia/Irkutsk')) > \
                    session.time_olympic.replace(tzinfo=pytz.timezone('Asia/Irkutsk')):
                count += 1
        for session in ResultsSessions.objects.filter(participant_identifier__in=list_identifier):
            count += 1
        return count

    def get_avg_points(self, obj):
        avg = 0.0
        if ResultsSessions.objects.filter(olympiad_theme=obj.theme).exists():
            for res in ResultsSessions.objects.filter(olympiad_theme=obj.theme):
                avg += res.total_points
            avg /= ResultsSessions.objects.filter(olympiad_theme=obj.theme).count()
        return avg

    class Meta:
        model = Olympiads
        fields = ['id', 'event_date', 'theme', 'complete_count', 'total_count', 'avg_points']


class ResultsCompletesSerializer(serializers.ModelSerializer):
    """Сериализация участников со статусом прохождения олимпиады"""
    is_complete = serializers.SerializerMethodField()
    have_results = serializers.SerializerMethodField()
    oo = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()

    def get_points(self, obj) -> int:
        if ResultsSessions.objects.filter(participant_identifier=obj.identifier).exists():
            return ResultsSessions.objects.get(participant_identifier=obj.identifier).total_points
        else:
            return 0

    def get_oo(self, obj):
        return Profiles.objects.get(id=obj.contact_person_id).oo_fullname

    def get_have_results(self, obj) -> bool:
        return ResultsSessions.objects.filter(participant_identifier=obj.identifier).exists()

    def get_is_complete(self, obj) -> str:
        if Sessions.objects.filter(participant_id=obj.identifier).exists():
            ses = Sessions.objects.get(participant_id=obj.identifier)
            if ses.time_olympic.replace(tzinfo=pytz.timezone('Asia/Irkutsk')) == \
                    ses.time_finish.replace(tzinfo=pytz.timezone('Asia/Irkutsk')):
                return 'В процессе'
            else:
                return 'Завершил прохождение'
        if self.get_have_results(obj):
            return 'Завершил прохождение'
        return 'Не проходил'

    class Meta:
        model = Apps
        fields = ['surname', 'name', 'group', 'identifier', 'oo', 'points', 'is_complete', 'have_results']