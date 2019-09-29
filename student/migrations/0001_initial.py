# Generated by Django 2.2 on 2019-08-16 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('first_name', models.CharField(default='', max_length=30)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=40)),
                ('registration_no', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=35)),
                ('dateofbirth', models.DateField(null=True)),
                ('branch', models.CharField(max_length=40)),
                ('gender', models.CharField(max_length=20)),
                ('yearofreg', models.CharField(default='', max_length=10)),
                ('monthofreg', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=20)),
                ('course_name', models.CharField(max_length=50)),
                ('credits', models.CharField(max_length=2)),
                ('year_of_course', models.CharField(default='', max_length=15)),
                ('semester', models.CharField(default='', max_length=15)),
                ('registration_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.StudentProfile')),
            ],
        ),
    ]
