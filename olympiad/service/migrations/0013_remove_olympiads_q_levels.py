# Generated by Django 4.1.4 on 2023-01-06 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0012_olympiadslevels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='olympiads',
            name='q_levels',
        ),
    ]
