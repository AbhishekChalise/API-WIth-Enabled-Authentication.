# Generated by Django 5.1.3 on 2024-12-03 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_deleted',
            field=models.BooleanField(default='False'),
            preserve_default=False,
        ),
    ]