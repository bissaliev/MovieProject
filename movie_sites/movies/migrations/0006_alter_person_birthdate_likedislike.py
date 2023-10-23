# Generated by Django 4.2.6 on 2023-10-19 13:33

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0002_remove_content_type_name"),
        ("movies", "0005_movie_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="birthdate",
            field=models.DateField(
                validators=[
                    django.core.validators.MaxValueValidator(
                        datetime.date(2023, 10, 19),
                        "Дата рождения не может быть больше нынешней!",
                    )
                ],
                verbose_name="Дата рождения",
            ),
        ),
        migrations.CreateModel(
            name="LikeDislike",
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
                (
                    "vote",
                    models.SmallIntegerField(
                        choices=[(1, "нравится"), (-1, "не нравится")],
                        verbose_name="Голос",
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_likes",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Лайк",
                "verbose_name_plural": "Лайки",
            },
        ),
    ]
