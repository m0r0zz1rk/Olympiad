import datetime

from django.db import models
from tinymce import models as tinymce_models


TYPES_CHOICES = (
    ('Развернутый ответ', 'Развернутый ответ'),
    ('Краткий ответ', 'Краткий ответ'),
    ('Соответствие', 'Соответствие'),
    ('Табличный', 'Табличный'),
    ('Классический', 'Классический')
)


class QuestionLevels(models.Model):
    """Модель уровней вопросов"""
    date_create = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата добавления уровня'
    )
    level = models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=150,
        verbose_name='Наименование уровня'
    )

    objects = models.Manager()

    def __str__(self):
        return self.level

    class Meta:
        verbose_name = 'Уровень вопросов'
        verbose_name_plural = 'Уровени вопросов'


class Olympiads(models.Model):
    """Модель олимпиад"""
    event_date = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата проведения'
    )
    theme = models.TextField(
        max_length=1000,
        blank=False,
        unique=True,
        verbose_name='Тема'
    )
    date_reg_start = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата начала регистрации заявок',
    )
    date_reg_end = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата окончания регистрации заявок'
    )
    time_complete = models.PositiveIntegerField(
        default=10,
        verbose_name='Время выполнения олимпиады (в минутах)'
    )

    objects = models.Manager()

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Олимпиада'
        verbose_name_plural = 'Олимпиады'


class OlympiadsLevels(models.Model):
    """Модель распределения уровней вопросов на олимпиадах"""
    olympiad = models.ForeignKey(
        Olympiads,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Олимпиада'
    )
    level = models.ForeignKey(
        QuestionLevels,
        on_delete=models.PROTECT,
        default=None,
        null=True,
        verbose_name='Уровень вопроса'
    )
    seq_number = models.PositiveIntegerField(
        default=1,
        verbose_name='Порядковый номер'
    )

    objects = models.Manager()

    def __str__(self):
        return f'{str(self.seq_number)}-й уровень вопроса'

    class Meta:
        verbose_name = 'Распределение уровня вопросов на олимпиаде'
        verbose_name_plural = 'Распределения уровней вопросов на олимпиадах'
        unique_together = ('olympiad', 'seq_number')


class Questions(models.Model):
    """Модель вопросов"""
    date_create = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата добавления вопроса'
    )
    level = models.ForeignKey(
        QuestionLevels,
        on_delete=models.PROTECT,
        default=None,
        null=True,
        verbose_name='Уровень вопроса'
    )
    question = tinymce_models.HTMLField(
        verbose_name='Вопрос'
    )
    type = models.CharField(
        max_length=50,
        choices=TYPES_CHOICES,
        default='Классическкий',
        verbose_name='Тип вопроса'
    )

    objects = models.Manager()

    def __str__(self):
        return f'Вопрос уровня "{self.level}" от {self.date_create.strftime("%d.%m.%Y")} г.'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class QuestionPossibleValues(models.Model):
    """Модель возможных значений к варианту ответа (тип вопроса - соответствие)"""
    question = models.ForeignKey(
        Questions,
        on_delete=models.CASCADE,
        null=False,
        default=1,
        verbose_name='Вопрос'
    )
    value = models.CharField(
        max_length=350,
        blank=False,
        verbose_name='Возможный вариант ответа'
    )

    objects = models.Manager()

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Возможный вариант ответа'
        verbose_name_plural = 'Возможные варианты ответа'


class QuestionColumns(models.Model):
    """Модель заголовков таблиц ответов на вопрос (тип вопроса - табличный)"""
    question = models.ForeignKey(
        Questions,
        on_delete=models.CASCADE,
        default=1,
        null=False,
        verbose_name='Вопрос'
    )
    seq_number = models.PositiveIntegerField(
        default=0,
        verbose_name='Последовательный номер'
    )
    column = models.CharField(
        max_length=350,
        verbose_name='Наименование столбца'
    )

    objects = models.Manager()

    def __str__(self):
        return f'{self.column} (к вопросу: {self.question})'

    class Meta:
        verbose_name = 'Столбец ответа к вопросу'
        verbose_name_plural = 'Столбцы ответов к вопросам'


class Answers(models.Model):
    """Модель ответов на вопросы"""
    question = models.ForeignKey(
        Questions,
        on_delete=models.CASCADE,
        default=1,
        null=False,
        verbose_name='Вопрос'
    )
    label = models.CharField(
        max_length=350,
        blank=False,
        default='Ответ:',
        verbose_name='Подпись к варианту ответа'
    )
    acc_correct = models.ForeignKey(
        QuestionPossibleValues,
        on_delete=models.PROTECT,
        null=True,
        default=None,
        verbose_name='Правильный вариант ответа (тип вопроса - соответствие)'
    )
    short_correct = models.CharField(
        max_length=350,
        default='Ответ',
        blank=False,
        verbose_name='Правильный вариант ответа (тип вопроса - краткий ответ)'
    )

    objects = models.Manager()

    def __str__(self):
        return f'{self.label} (к вопросу:{self.question})'

    class Meta:
        verbose_name = 'Ответ к вопросу'
        verbose_name_plural = 'Ответы к вопросам'


class ChoicesAnswers(models.Model):
    """Модель ответов на вопросы (тип вопроса - классический)"""
    question = models.ForeignKey(
        Questions,
        on_delete=models.CASCADE,
        default=1,
        null=False,
        verbose_name='Вопрос'
    )
    choice = models.CharField(
        max_length=350,
        blank=False,
        default='Ответ:',
        verbose_name='Вариант ответа'
    )
    correct = models.BooleanField(
        default=False,
        verbose_name='Праваильный ответ'
    )

    objects = models.Manager()

    def __str__(self):
        return self.choice

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'


class TableAnswers(models.Model):
    """Модель правильных ответов на вопросы (тип вопроса - табличный)"""
    label = models.CharField(
        max_length=350,
        blank=False,
        default='Лэйбл',
        verbose_name='Подпись к строке ответов'
    )
    column = models.ForeignKey(
        QuestionColumns,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Столбец'
    )
    seq_number = models.PositiveIntegerField(
        default=0,
        verbose_name='Последовательный номер'
    )
    correct = models.CharField(
        max_length=350,
        blank=False,
        default='Ответ',
        verbose_name='Правильный ответ'
    )

    objects = models.Manager()

    def __str__(self):
        return f'Правильный ответ к "{self.label}" , столбец "{self.column}"'

    class Meta:
        verbose_name = 'Ответ к табличному типу вопроса'
        verbose_name_plural = 'Ответы к табличному типу вопроса'


class ResultsSessions(models.Model):
    """Модель сессий для результатов олимпиад"""
    olympiad_theme = models.CharField(
        max_length=1000,
        blank=False,
        verbose_name='Тема'
    )
    event_date = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата проведения'
    )
    participant_surname = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Фамилия участника'
    )
    participant_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Имя участника'
    )
    participant_identifier = models.CharField(
        max_length=11,
        blank=False,
        unique=True,
        verbose_name='Идентификатор участника'
    )
    participant_oo = models.TextField(
        max_length=500,
        blank=False,
        null=False,
        verbose_name='Полное наименование образовательного учреждения участника'
    )
    participant_start = models.DateTimeField(
        default=datetime.datetime.now(),
        verbose_name='Время начала прохождения олимпиады участником'
    )
    participant_end = models.DateTimeField(
        default=datetime.datetime.now(),
        verbose_name='Время окончания прохождения олимпиады участником'
    )
    total_points = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество баллов, полученное пользователем'
    )

    objects = models.Manager()

    def __str__(self):
        return f'{self.participant_surname} {self.participant_name} ({self.olympiad_theme})'

    class Meta:
        verbose_name = 'Сессия участника олимпиады'
        verbose_name_plural = 'Сессии участников олимпиад'


class ResultsQuestions(models.Model):
    """Модель ответов на вопросы"""
    result_session = models.ForeignKey(
        ResultsSessions,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Сессия участника'
    )
    question_theme = models.CharField(
        blank=False,
        null=False,
        max_length=150,
        verbose_name='Тема вопроса'
    )
    question = tinymce_models.HTMLField(
        verbose_name='Вопрос'
    )
    question_id = models.PositiveIntegerField(
        default=0,
        verbose_name='ID вопроса'
    )
    answer_id = models.PositiveIntegerField(
        default=0,
        verbose_name='ID ответа'
    )
    answer_participant = models.CharField(
        max_length=350,
        blank=True,
        default='',
        verbose_name='Ответ участника'
    )
    answer_detail_participant = models.TextField(
        max_length=30000,
        default='',
        verbose_name='Ответ участника на вопрос типа "Развернутый ответ"'
    )
    points = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество баллов, полученное участником за вопрос'
    )

    objects = models.Manager()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Ответ на вопрос учатника олимпиады'
        verbose_name_plural = 'Ответы на вопросы учатников олимпиад'

