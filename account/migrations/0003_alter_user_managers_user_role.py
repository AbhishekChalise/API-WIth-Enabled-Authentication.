# Generated by Django 5.1.3 on 2024-12-05 10:11

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_table'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('teacher', 'teacher'), ('admin', 'Admin')], default='student', max_length=10, null=True),
        ),
    ]