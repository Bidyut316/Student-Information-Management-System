# Generated by Django 3.0.2 on 2020-07-05 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import studentinfo.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='department_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StudentBasicInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_roll', models.SmallIntegerField()),
                ('semester', models.CharField(choices=[('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th'), ('6th', '6th')], max_length=10)),
                ('blod_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=10)),
                ('session', models.CharField(blank=True, max_length=50)),
                ('photo', models.ImageField(null=True, upload_to=studentinfo.models.upload_image_path)),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True)),
                ('data_status', models.CharField(choices=[('verify', 'verify'), ('not verify', 'not verify')], max_length=50)),
                ('student_status', models.CharField(choices=[('current student', 'current stucent'), ('old student', 'old student')], max_length=50)),
                ('department_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='studentinfo.department_list')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vill', models.CharField(blank=True, max_length=50)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('dist', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('pin', models.CharField(max_length=10)),
                ('address_type', models.CharField(choices=[('Current Address', 'Current Address'), ('Permanent Address', 'Permanent Address')], default=None, max_length=50)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AcademicInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(blank=True, max_length=50)),
                ('university_name', models.CharField(blank=True, max_length=50)),
                ('collage_name', models.CharField(blank=True, max_length=50)),
                ('passing_year', models.PositiveSmallIntegerField()),
                ('Percentage', models.FloatField(blank=True, max_length=50)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
