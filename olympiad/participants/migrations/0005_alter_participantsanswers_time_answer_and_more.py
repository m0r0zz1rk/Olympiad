# Generated by Django 4.1.4 on 2023-01-09 01:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0004_participantsanswers_seq_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantsanswers',
            name='time_answer',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 9, 9, 15, 19, 725341), verbose_name='Время ответа'),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='time_finish',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 9, 9, 15, 19, 724341), verbose_name='Время окончания прохождения олимпиады'),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='time_olympic',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 9, 9, 15, 19, 724341), verbose_name='Время начала прохождения олимпиады'),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='time_startpage',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 9, 9, 15, 19, 724341), verbose_name='Время входа в АИС'),
        ),
    ]