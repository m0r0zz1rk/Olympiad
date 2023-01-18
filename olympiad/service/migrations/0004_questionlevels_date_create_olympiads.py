# Generated by Django 4.1.4 on 2022-12-31 05:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_questioncolumns_questionpossiblevalues_answers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionlevels',
            name='date_create',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата добавления уровня'),
        ),
        migrations.CreateModel(
            name='Olympiads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateField(default=datetime.date.today, verbose_name='Дата проведения')),
                ('theme', models.TextField(max_length=1000, verbose_name='Тема')),
                ('date_reg_start', models.DateField(default=datetime.date.today, verbose_name='Дата начала регистрации заявок')),
                ('date_reg_end', models.DateField(default=datetime.date.today, verbose_name='Дата окончания регистрации заявок')),
                ('q_levels', models.ManyToManyField(to='service.questionlevels', verbose_name='Уровни вопросов')),
            ],
            options={
                'verbose_name': 'Олимпиада',
                'verbose_name_plural': 'Олимпиады',
            },
        ),
    ]
