# Generated by Django 4.1.4 on 2023-01-07 07:49

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service', '0016_olympiads_time_complete'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sessions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant_id', models.CharField(max_length=11, unique=True, verbose_name='ID участника')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('olympiad_id', models.PositiveIntegerField(default=1, verbose_name='ID олимпиады')),
                ('time_startpage', models.DateTimeField(default=datetime.datetime(2023, 1, 7, 15, 49, 25, 120377), verbose_name='Время входа в АИС')),
                ('time_olympic', models.DateTimeField(default=datetime.datetime(2023, 1, 7, 15, 49, 25, 120377), verbose_name='Время начала прохождения олимпиады')),
                ('time_finish', models.DateTimeField(default=datetime.datetime(2023, 1, 7, 15, 49, 25, 120377), verbose_name='Время окончания прохождения олимпиады')),
            ],
            options={
                'verbose_name': 'Сессия участника олимпиады',
                'verbose_name_plural': 'Сессии участников олимпиады',
            },
        ),
        migrations.CreateModel(
            name='ParticipantsAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_detailed', models.TextField(max_length=30000, verbose_name='Ответ участника на вопрос типа "Развернутый ответ"')),
                ('answer', models.CharField(max_length=500, verbose_name='Ответ участника')),
                ('time_answer', models.DateTimeField(default=datetime.datetime(2023, 1, 7, 15, 49, 25, 121374), verbose_name='Время ответа')),
                ('time_to_end', models.PositiveIntegerField(default=0, verbose_name='Время до конца олимпиады (в секундах)')),
                ('question', models.ForeignKey(default=1, null=None, on_delete=django.db.models.deletion.CASCADE, to='service.questions', verbose_name='Вопрос')),
                ('session', models.ForeignKey(default=1, null=None, on_delete=django.db.models.deletion.CASCADE, to='participants.sessions', verbose_name='Сессия участника')),
            ],
            options={
                'verbose_name': 'Ответ участника олимпиады',
                'verbose_name_plural': 'Ответы участника олимпиады',
            },
        ),
    ]
