# Generated by Django 3.1 on 2020-09-23 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_auto_20200922_1309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty',
            name='phoneNumber',
        ),
    ]