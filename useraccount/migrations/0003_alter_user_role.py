# Generated by Django 4.2.2 on 2023-09-28 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0002_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher')], default='student', max_length=50),
        ),
    ]
