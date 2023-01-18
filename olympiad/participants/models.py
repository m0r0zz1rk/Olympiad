import datetime
import uuid

from django.db import models

from service.models import Questions


class Sessions(models.Model):
    """Модель сессий участников олимпиад"""
    participant_id = models.CharField(
        max_length=11,
        unique=True,
        verbose_name='ID участника'
    )
    unique_id = models.UUIDField(
        default=uuid.uuid4,
        editable=True,
        unique=True
    )
    olympiad_id = models.PositiveIntegerField(
        default=1,
        verbose_name='ID олимпиады'
    )
    time_startpage = models.DateTimeField(
        default=datetime.datetime.now(),
        verbose_name='Время входа в АИС'
    )
    time_olympic = models.DateTimeField(
        default=datetime.datetime.now(),
        verbose_name='Время начала прохождения олимпиады'
    )
    time_stop = models.PositiveIntegerField(
        default=0,
        verbose_name='Оставшееся время выполнения олимпиады (в случае дисконнекта)'
    )
    time_finish = models.DateTimeField(
        default=datetime.datetime.now(),
        verbose_name='Время окончания прохождения олимпиады'
    )

    objects = models.Manager()

    def __str__(self):
        return self.participant_id

    class Meta:
        verbose_name = 'Сессия участника олимпиады'
        verbose_name_plural = 'Сессии участников олимпиады'


class ParticipantsAnswers(models.Model):
    """Модель ответов участников олимпиад"""
    session = models.PositiveIntegerField(
        default=1,
        verbose_name='ID сессии'
    )
    seq_number = models.PositiveIntegerField(
        default=1,
        verbose_name='Порядковый номер'
    )
    question_id = models.PositiveIntegerField(
        default=1,
        verbose_name='ID вопроса'
    )
    answer_id = models.PositiveIntegerField(
        default=0,
        verbose_name='ID ответа'
    )
    answer_detailed = models.TextField(
        max_length=30000,
        default='',
        verbose_name='Ответ участника на вопрос типа "Развернутый ответ"'
    )
    answer = models.CharField(
        max_length=500,
        default='',
        verbose_name='Ответ участника'
    )
    time_answer = models.DateTimeField(
        default=datetime.datetime.now(),
        verbose_name='Время ответа'
    )
    time_to_end = models.PositiveIntegerField(
        default=0,
        verbose_name='Время до конца олимпиады (в секундах)'
    )

    objects = models.Manager()

    def __str__(self):
        return str(self.session)

    class Meta:
        verbose_name = 'Ответ участника олимпиады'
        verbose_name_plural = 'Ответы участника олимпиады'

