from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

kind_choices = (
    ('Дополнительное', 'Дополнительное'),
    ('Профессиональное', 'Профессиональное'),
    ('Общее', 'Общее'),
)


class Profiles(models.Model):
    """Модель профилей пользователей"""
    dj_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь Django'
    )
    surname = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Фамилия'
    )
    name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Имя'
    )
    patronymic = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Отчество'
    )
    oo_fullname = models.TextField(
        max_length=500,
        blank=False,
        null=False,
        verbose_name='Полное наименование образовательного учреждения'
    )
    oo_address = models.TextField(
        max_length=750,
        blank=False,
        null=False,
        verbose_name='Физический адрес образовательного учреждения'
    )
    position = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Должность'
    )
    phone = models.CharField(
        max_length=20,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Контактный телефон'
    )

    objects = models.Manager()

    def __str__(self):
        if self.patronymic == '':
            return f'{self.surname} {self.name}'
        else:
            return f'{self.surname} {self.name} {self.patronymic}'

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class Apps(models.Model):
    """Модель заявок на участие в олимпиаде"""
    date_create = models.DateField(
        auto_now_add=True,
        verbose_name='Дата подачи заявки'
    )
    contact_person = models.ForeignKey(
        Profiles,
        on_delete=models.PROTECT,
        default='*Удаленный пользователь*',
        verbose_name='Контактное лицо'
    )
    surname = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Фамилия'
    )
    name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Имя'
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(100)],
        verbose_name='Возраст'
    )
    study_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        verbose_name='Год обучения'
    )
    study_kind = models.CharField(
        choices=kind_choices,
        max_length=50,
        verbose_name='Вид образования'
    )
    study_duration = models.PositiveIntegerField(
        validators=[MinValueValidator(4), MaxValueValidator(8)],
        verbose_name='Срок реализации программы обучения'
    )
    teacher = models.CharField(
        max_length=500,
        blank=False,
        verbose_name='ФИО преподавателя'
    )
    group = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Группа'
    )
    identifier = models.CharField(
        max_length=11,
        blank=False,
        unique=True,
        verbose_name='Идентификатор'
    )

    objects = models.Manager()

    def __str__(self):
        return f'{self.surname} {self.name} (ID: {self.identifier})'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
