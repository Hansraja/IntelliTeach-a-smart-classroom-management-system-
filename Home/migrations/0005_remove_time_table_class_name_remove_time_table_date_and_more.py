# Generated by Django 5.0.2 on 2024-04-20 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0004_student_marks_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='time_table',
            name='class_name',
        ),
        migrations.RemoveField(
            model_name='time_table',
            name='date',
        ),
        migrations.RemoveField(
            model_name='time_table',
            name='section',
        ),
        migrations.RemoveField(
            model_name='time_table',
            name='teacher',
        ),
    ]
