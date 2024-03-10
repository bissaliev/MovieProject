import uuid
from pathlib import Path

from django.db import models
from django.db.models import Sum
from django.core.validators import MaxValueValidator
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import (
    GenericForeignKey, GenericRelation
)

from .fields import WEBPField


User = get_user_model()


def get_image_folder(instance, filename):
    """Функция для определения пути изображений."""
    return f"{instance.__class__.__name__}/{uuid.uuid4().hex}.webp"


class Person(models.Model):
    """Актеры и режиссеры."""
    M = "М"
    F = "F"
    U = "U"
    GENDER_CHOICES = [(M, "Мужчина"), (F, "Женщина"), (U, "Неизвестно")]

    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100, db_index=True)
    birthdate = models.DateField(
        "Дата рождения",
        validators=[
            MaxValueValidator(
                timezone.now().date(),
                "Дата рождения не может быть больше нынешней!"
            )
        ],
    )
    description = models.TextField("Описание", blank=True, null=True)
    picture = WEBPField(
        "Фото", upload_to=get_image_folder, blank=True, null=True
    )
    gender = models.CharField(
        "Гендер",
        max_length=1,
        choices=GENDER_CHOICES,
        default=U,
    )
    country = models.ForeignKey(
        to="Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Страна",
        related_name="%(class)ss",
    )
    votes = GenericRelation(to="LikeDislike", related_query_name="person_vote")
    bookmarks = GenericRelation(
        to="Bookmark", related_query_name="person_bookmark"
    )

    class Meta:
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"
        ordering = ["last_name", "first_name"]
        constraints = [
            models.UniqueConstraint(
                fields=("last_name", "first_name"),
                name="unique_last_first_name"
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("movies:person_detail", kwargs={"person_id": self.id})

    @property
    def get_age(self):
        today = timezone.now().date()
        age = today.year - self.birthdate.year
        - (
            (today.month, today.day)
            < (self.birthdate.month, self.birthdate.day)
        )
        return age

    def get_like_count(self):
        return self.votes.filter(vote__gt=0).count()

    def get_dislike_count(self):
        return self.votes.filter(vote__lt=0).count()

    @property
    def get_like_rating(self):
        return self.votes.values(
            "vote").aggregate(Sum("vote")).get("vote__sum")


class AbstractCategory(models.Model):
    """Абстрактная модель для Category, Genre, Country."""

    name = models.CharField("Название", max_length=100, unique=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name


class Country(AbstractCategory):
    """Страны."""

    class Meta(AbstractCategory.Meta):
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def get_absolute_url(self):
        return reverse("movies:country_detail", kwargs={"country_id": self.id})


class Category(AbstractCategory):
    """Категории фильмов."""

    slug = models.SlugField("Идентификатор", max_length=100, unique=True)

    class Meta(AbstractCategory.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse(
            "movies:category_detail", kwargs={"category_slug": self.slug}
        )


class Genre(AbstractCategory):
    """Жанры фильмов."""

    slug = models.SlugField("Идентификатор", max_length=100, unique=True)

    class Meta(AbstractCategory.Meta):
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def get_absolute_url(self):
        return reverse("movies:genre_detail", kwargs={"slug": self.slug})


class Movie(models.Model):
    """Фильмы."""

    name = models.CharField("Название", max_length=100, db_index=True)
    description = models.TextField("Описание", blank=True, null=True)
    release_year = models.PositiveSmallIntegerField(
        "Год выпуска"
    )
    poster = WEBPField(
        "Постер", upload_to=get_image_folder, null=True, blank=True
    )
    category = models.ForeignKey(
        to="Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movies"
    )
    genres = models.ManyToManyField(
        to="Genre",
        related_name="genre_movies",
        verbose_name="Жанры фильма",
        blank=True
    )
    countries = models.ManyToManyField(
        to="Country",
        related_name="country_movies",
        verbose_name="Страны производства",
        blank=True,
    )
    actors = models.ManyToManyField(
        to="Person",
        through="MovieActor",
        related_name="actor_movies",
        verbose_name="Актеры фильма",
        blank=True,
    )
    directors = models.ManyToManyField(
        to="Person",
        related_name="director_movies",
        verbose_name="Режиссеры фильма",
        blank=True,
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    rating = models.FloatField(null=True, blank=True, default=0)
    bookmarks = GenericRelation(to="Bookmark", related_query_name="movie")

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ["name", "release_year"]

    def __str__(self):
        return f"{self.name}({self.release_year})"

    def get_absolute_url(self):
        return reverse("movies:movie_detail", kwargs={"movie_id": self.id})

    def get_comments(self):
        return self.comments.filter(major__isnull=True)

    @property
    def get_average_rating(self):
        """Метод для вычисление среднего рейтинга по сайту."""

        return self.ratings.aggregate(avg=models.Avg("score")).get("avg")


class MovieActor(models.Model):
    """
    Промежуточная модель для фильмов и актеров дополнительным полем role
    (роль в фильме).
    """
    movie = models.ForeignKey(
        to="Movie",
        on_delete=models.CASCADE,
        related_name="movies",
        verbose_name="Фильм"
    )
    actor = models.ForeignKey(
        to="Person",
        on_delete=models.CASCADE,
        related_name="actors",
        verbose_name="Актер"
    )
    role = models.CharField("Роль", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Фильм-Актер"
        verbose_name_plural = "Фильмы-Актеры"

    def __str__(self):
        return f"{self.movie} - {self.actor}"


class Rating(models.Model):
    """Рейтинг."""
    RATING_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    ]
    movie = models.ForeignKey(
        to="Movie",
        on_delete=models.CASCADE,
        verbose_name="Фильм",
        related_name="ratings"
    )
    score = models.PositiveSmallIntegerField(
        "Оценка",
        choices=RATING_CHOICES
    )
    ip = models.CharField("IP адрес", max_length=15)

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

    def __str__(self):
        return f"{self.movie} - {self.score}"


class Comment(models.Model):
    """Комментарии."""

    email = models.EmailField("Email")
    name = models.CharField("Имя", max_length=100)
    movie = models.ForeignKey(
        to="Movie",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Фильм",
    )
    text = models.TextField("Текст комментария")
    major = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Старший комментарий",
        related_name="children"
    )
    pub_date = models.DateTimeField("Время публикации", auto_now_add=True)
    votes = GenericRelation(to="LikeDislike", related_query_name="comment")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-pub_date"]

    def __str__(self):
        return f"{self.name} - {self.movie}"

    def get_like_count(self):
        return self.votes.filter(vote__gt=0).count()

    def get_dislike_count(self):
        return self.votes.filter(vote__lt=0).count()


class LikeDislike(models.Model):
    """Модель лайков и дизлайков."""
    class Vote(models.IntegerChoices):
        LIKE = 1, "нравится"
        DISLIKE = -1, "не нравится"

    vote = models.SmallIntegerField("Голос", choices=Vote.choices, null=True)
    user = models.ForeignKey(
        User, related_name="user_likes",
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return f"{self.user} - {self.content_type}: ({self.vote})"


class Bookmark(models.Model):
    """Закладки."""
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="bookmarks",
        verbose_name="Пользователь"
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="bookmarks",
        verbose_name="Закладка"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = "Закладка"
        verbose_name_plural = "Закладки"

    def __str__(self):
        return f"{self.user} - {self.content_type}"
