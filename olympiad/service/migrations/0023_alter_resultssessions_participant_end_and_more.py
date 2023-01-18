# Generated by Django 4.0.3 on 2023-01-13 01:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0022_alter_resultssessions_participant_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultssessions',
            name='participant_end',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 13, 9, 42, 27, 638311), verbose_name='Время окончания прохождения олимпиады участником'),
        ),
        migrations.AlterField(
            model_name='resultssessions',
            name='participant_start',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 13, 9, 42, 27, 638311), verbose_name='Время начала прохождения олимпиады участником'),
        ),
    ]
