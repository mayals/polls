# Generated by Django 5.0.3 on 2024-03-27 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='poll_question',
        ),
    ]