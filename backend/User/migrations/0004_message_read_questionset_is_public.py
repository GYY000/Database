# Generated by Django 4.2.3 on 2023-11-07 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("User", "0003_remove_question_answer_questionset_profile_photo_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="read",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="questionset",
            name="is_public",
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]