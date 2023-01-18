from rest_framework import serializers

from participants.models import ParticipantsAnswers
from service.models import Olympiads, Questions
from users.models import Apps


class ParticipantSerializer(serializers.ModelSerializer):
    """Сериализация данных об участнике для стартовой страницы"""

    class Meta:
        model = Apps
        fields = ('surname', 'name', 'age', 'group', 'teacher')


class OlypmicSerializer(serializers.ModelSerializer):
    """Сериализация данных об олимпиаде для стартовой страницы"""

    class Meta:
        model = Olympiads
        fields = ('event_date', 'theme', 'time_complete')


class OlympicQuestionsSerializer(serializers.ModelSerializer):
    """Сериализация вопросов для участников олимпиад"""
    level = serializers.SlugRelatedField(
        slug_field='level',
        read_only=True
    )

    class Meta:
        model = Questions
        fields = ('level', 'question')


class ParticipantAnswerFullSerializer(serializers.ModelSerializer):
    """Сериализация ответов участников олимпиад"""

    class Meta:
        model = ParticipantsAnswers
        exclude = ('time_to_end',)