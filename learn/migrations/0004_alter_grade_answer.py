# Generated by Django 4.1.2 on 2022-10-23 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("learn", "0003_remove_grade_content_type_remove_grade_object_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="grade",
            name="answer",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="grade",
                to="learn.answertask",
            ),
        ),
    ]