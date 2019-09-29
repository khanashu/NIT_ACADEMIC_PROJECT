# Generated by Django 2.2 on 2019-08-16 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dean', '0001_initial'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarksEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid_sem', models.IntegerField(default=0)),
                ('end_sem', models.IntegerField(default=0)),
                ('course_id', models.CharField(max_length=20)),
                ('year', models.CharField(max_length=20)),
                ('semester', models.CharField(max_length=12)),
                ('total_marks', models.IntegerField(default=0)),
                ('Grade', models.CharField(max_length=5)),
                ('Accepted', models.CharField(default=0, max_length=2)),
                ('registration_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.StudentProfile')),
            ],
        ),
        migrations.CreateModel(
            name='FacultyNotifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=10)),
                ('year', models.CharField(max_length=14)),
                ('semester', models.CharField(max_length=12)),
                ('read', models.CharField(default=0, max_length=2)),
                ('accepted', models.CharField(default=0, max_length=2)),
                ('employee_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dean.AddFaculty')),
            ],
        ),
    ]
