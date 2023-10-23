# Generated by Django 4.2.6 on 2023-10-20 13:05

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("movies", "0007_alter_likedislike_vote"),
    ]

    operations = [
        migrations.AlterField(
            model_name="likedislike",
            name="content_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="birthdate",
            field=models.DateField(
                validators=[
                    django.core.validators.MaxValueValidator(
                        datetime.date(2023, 10, 20),
                        "Дата рождения не может быть больше нынешней!",
                    )
                ],
                verbose_name="Дата рождения",
            ),
        ),
    ]
