# Generated by Django 4.2.6 on 2023-10-25 07:54

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0010_alter_movie_release_year_alter_person_birthdate_and_more"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="bookmark",
            managers=[
                ("bookmark_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name="person",
            name="birthdate",
            field=models.DateField(
                validators=[
                    django.core.validators.MaxValueValidator(
                        datetime.date(2023, 10, 25),
                        "Дата рождения не может быть больше нынешней!",
                    )
                ],
                verbose_name="Дата рождения",
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="gender",
            field=models.CharField(
                choices=[("М", "Мужчина"), ("F", "Женщина"), ("U", "Неизвестно")],
                default="U",
                max_length=1,
                verbose_name="Гендер",
            ),
        ),
    ]
