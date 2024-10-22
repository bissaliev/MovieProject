# Generated by Django 4.2.6 on 2023-10-12 02:42

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Название"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=100, unique=True, verbose_name="Идентификатор"
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Country",
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
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Название"
                    ),
                ),
            ],
            options={
                "verbose_name": "Страна",
                "verbose_name_plural": "Страны",
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Genre",
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
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Название"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=100, unique=True, verbose_name="Идентификатор"
                    ),
                ),
            ],
            options={
                "verbose_name": "Жанр",
                "verbose_name_plural": "Жанры",
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Movie",
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
                    "name",
                    models.CharField(
                        db_index=True, max_length=100, verbose_name="Название"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                (
                    "release_year",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(
                                2023, "Год выпуска не может быть больше нынешнего!"
                            )
                        ],
                        verbose_name="Год выпуска",
                    ),
                ),
                (
                    "poster",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="movies/%Y/%m/%d",
                        verbose_name="Постер",
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата публикации"
                    ),
                ),
            ],
            options={
                "verbose_name": "Фильм",
                "verbose_name_plural": "Фильмы",
                "ordering": ["name", "release_year"],
            },
        ),
        migrations.CreateModel(
            name="Person",
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
                ("first_name", models.CharField(max_length=100, verbose_name="Имя")),
                (
                    "last_name",
                    models.CharField(
                        db_index=True, max_length=100, verbose_name="Фамилия"
                    ),
                ),
                (
                    "birthdate",
                    models.DateField(
                        validators=[
                            django.core.validators.MaxValueValidator(
                                datetime.date(2023, 10, 12),
                                "Дата рождения не может быть больше нынешней!",
                            )
                        ],
                        verbose_name="Дата рождения",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="persons/%Y/%m/%d",
                        verbose_name="Фото",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("М", "Мужчина"), ("F", "Женщина"), ("U", "Unknown")],
                        default="U",
                        max_length=1,
                        verbose_name="Гендер",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)ss",
                        to="movies.country",
                        verbose_name="Страна",
                    ),
                ),
            ],
            options={
                "verbose_name": "Персона",
                "verbose_name_plural": "Персоны",
                "ordering": ["last_name", "first_name"],
            },
        ),
        migrations.CreateModel(
            name="MovieActor",
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
                    "role",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Роль"
                    ),
                ),
                (
                    "actor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="actors",
                        to="movies.person",
                        verbose_name="Актер",
                    ),
                ),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="movies",
                        to="movies.movie",
                        verbose_name="Фильм",
                    ),
                ),
            ],
            options={
                "verbose_name": "Фильм-Актер",
                "verbose_name_plural": "Фильмы-Актеры",
            },
        ),
        migrations.AddField(
            model_name="movie",
            name="actors",
            field=models.ManyToManyField(
                blank=True,
                related_name="actor_movies",
                through="movies.MovieActor",
                to="movies.person",
                verbose_name="Актеры фильма",
            ),
        ),
        migrations.AddField(
            model_name="movie",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="movies.category",
            ),
        ),
        migrations.AddField(
            model_name="movie",
            name="countries",
            field=models.ManyToManyField(
                blank=True,
                related_name="country_movies",
                to="movies.country",
                verbose_name="Страны производства",
            ),
        ),
        migrations.AddField(
            model_name="movie",
            name="directors",
            field=models.ManyToManyField(
                blank=True,
                related_name="director_movies",
                to="movies.person",
                verbose_name="Режиссеры фильма",
            ),
        ),
        migrations.AddField(
            model_name="movie",
            name="genres",
            field=models.ManyToManyField(
                blank=True,
                related_name="genre_movies",
                to="movies.genre",
                verbose_name="Жанры фильма",
            ),
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("name", models.CharField(max_length=100, verbose_name="Имя")),
                ("text", models.TextField(verbose_name="Текст комментария")),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время публикации"
                    ),
                ),
                (
                    "major",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="majors",
                        to="movies.comment",
                        verbose_name="Старший комментарий",
                    ),
                ),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="movies.movie",
                        verbose_name="Фильм",
                    ),
                ),
            ],
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
                "ordering": ["-pub_date"],
            },
        ),
        migrations.AddConstraint(
            model_name="person",
            constraint=models.UniqueConstraint(
                fields=("last_name", "first_name"), name="unique_last_first_name"
            ),
        ),
    ]
