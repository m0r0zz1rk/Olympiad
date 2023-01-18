# Generated by Django 4.0.3 on 2023-01-11 12:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0020_remove_resultsquestions_answer_correct_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultsquestions',
            name='answer_id',
            field=models.PositiveIntegerField(default=0, verbose_name='ID ответа'),
        ),
        migrations.AddField(
            model_name='resultsquestions',
            name='question_id',
            field=models.PositiveIntegerField(default=0, verbose_name='ID вопроса'),
        ),
        migrations.AlterField(
            model_name='resultssessions',
            name='participant_end',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 11, 20, 49, 49, 522072), verbose_name='Время окончания прохождения олимпиады участником'),
        ),
        migrations.AlterField(
            model_name='resultssessions',
            name='participant_start',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 11, 20, 49, 49, 522072), verbose_name='Время начала прохождения олимпиады участником'),
        ),
    ]
