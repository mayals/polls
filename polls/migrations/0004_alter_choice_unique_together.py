# Generated by Django 5.0.3 on 2024-03-15 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_alter_choice_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='choice',
            unique_together=set(),
        ),
    ]