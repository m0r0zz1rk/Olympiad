# Generated by Django 4.1.4 on 2022-12-26 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apps',
            name='group',
            field=models.CharField(max_length=150, verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='apps',
            name='identifier',
            field=models.CharField(max_length=11, unique=True, verbose_name='Идентификатор'),
        ),
        migrations.AlterField(
            model_name='apps',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='apps',
            name='study_kind',
            field=models.CharField(choices=[('Дополнительное', 'Дополнительное'), ('Профессиональное', 'Профессиональное'), ('Общее', 'Общее')], max_length=50, verbose_name='Вид образования'),
        ),
        migrations.AlterField(
            model_name='apps',
            name='surname',
            field=models.CharField(max_length=150, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='apps',
            name='teacher',
            field=models.CharField(max_length=500, verbose_name='ФИО преподавателя'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='oo_address',
            field=models.TextField(max_length=750, verbose_name='Физический адрес образовательного учреждения'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='oo_fullname',
            field=models.TextField(max_length=500, verbose_name='Полное наименование образовательного учреждения'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='patronymic',
            field=models.CharField(blank=True, max_length=150, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='phone',
            field=models.CharField(max_length=20, unique=True, verbose_name='Контактный телефон'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='position',
            field=models.CharField(max_length=150, verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='surname',
            field=models.CharField(max_length=150, verbose_name='Фамилия'),
        ),
    ]
