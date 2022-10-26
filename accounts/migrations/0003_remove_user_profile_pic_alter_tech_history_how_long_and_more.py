# Generated by Django 4.1 on 2022-10-21 22:23

import accounts.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_tech_history_how_long_alter_user_gender"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="profile_pic",
        ),
        migrations.AlterField(
            model_name="tech_history",
            name="how_long",
            field=models.CharField(
                choices=[
                    ("1-3", "Between 1-3 years"),
                    ("1", "Less than one year"),
                    ("3-5", "Between 3-5 years"),
                    ("5+", "5 years+"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(
                max_length=14, validators=[accounts.validators.phone_validator]
            ),
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("profile_pic", models.ImageField(upload_to="profile_pictures")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
