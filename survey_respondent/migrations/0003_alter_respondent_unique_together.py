# Generated by Django 4.2 on 2024-09-30 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_survey_expires_at'),
        ('survey_respondent', '0002_remove_respondent_last_question_id_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='respondent',
            unique_together={('survey', 'user_id')},
        ),
    ]
