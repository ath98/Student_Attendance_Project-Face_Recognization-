# Generated by Django 3.1 on 2020-09-24 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_remove_faculty_phonenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='password',
            field=models.CharField(max_length=200, null=True),
        ),
    ]