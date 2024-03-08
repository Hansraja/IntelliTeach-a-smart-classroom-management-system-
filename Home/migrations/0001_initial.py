# Generated by Django 5.0.2 on 2024-03-08 04:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Admin', '0004_rename_department_faculty_subject_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mst1', models.IntegerField(blank=True, null=True)),
                ('mst2', models.IntegerField(blank=True, null=True)),
                ('assignment', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_marks', to='Admin.student')),
            ],
            options={
                'db_table': 'student_marks',
            },
        ),
        migrations.CreateModel(
            name='Student_Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=10000, null=True)),
                ('tag', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_read', models.BooleanField(default=False)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_messages', to='Admin.student')),
            ],
            options={
                'db_table': 'student_messages',
            },
        ),
        migrations.CreateModel(
            name='Teacher_Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=10000, null=True)),
                ('tag', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ManyToManyField(related_name='teacher_messages', to='Admin.faculty')),
            ],
            options={
                'db_table': 'teacher_messages',
            },
        ),
        migrations.CreateModel(
            name='Time_Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time_from', models.TimeField(blank=True, null=True)),
                ('time_to', models.TimeField(blank=True, null=True)),
                ('subject', models.CharField(blank=True, max_length=255, null=True)),
                ('class_name', models.CharField(blank=True, max_length=255, null=True)),
                ('section', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_timetable', to='Admin.faculty')),
            ],
            options={
                'db_table': 'time_table',
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_attendance', to='Admin.student')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_attendance', to='Admin.faculty')),
                ('time', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='time_attendance', to='Home.time_table')),
            ],
            options={
                'db_table': 'attendance',
            },
        ),
    ]
