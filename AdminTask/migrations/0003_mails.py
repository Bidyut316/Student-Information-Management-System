# Generated by Django 3.0.2 on 2020-07-28 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminTask', '0002_deleterecords_data_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=1000)),
                ('message', models.CharField(max_length=20000)),
                ('document', models.FileField(upload_to='documents/')),
            ],
        ),
    ]
