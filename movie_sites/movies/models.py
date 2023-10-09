from django.db import models
from django.core.validators import MaxValueValidator
from django.urls import reverse
from django.utils import timezone


GENDER_CHOICES = [("М", "Мужчина"), ("Ж", "Женщина"), ("U", "Unknown")]


def get_upload_path(instance, filename):
    """Функция для определения пути изображений."""
    today = timezone.now().strftime("%Y/%m/%d")
    return f"{instance.__class__.__name__}/{today}/{filename}"


class AbstractPerson(models.Model):
    """Абстрактная модель."""

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
    picture = models.ImageField(
        "Фото",
        upload_to=get_upload_path,
        blank=True,
        null=True,
    )
    gender = models.CharField(
        "Гендер",
        max_length=1,
        choices=GENDER_CHOICES,
        default="U",
    )
    country = models.ForeignKey(
        to="Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Страна",
        related_name="%(class)ss",
    )

    class Meta:
        abstract = True
        ordering = ["last_name", "first_name"]
        # constraints = [
            # models.UniqueConstraint(
                # fields=("last_name", "first_name"),
                # name=f"unique_name_{get_class_name}"
            # )
        # ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    # def get_class_name(self):
        # return self.__class__.__name__


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


class Actor(AbstractPerson):
    """Актеры."""

    class Meta(AbstractPerson.Meta):
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"

    def get_absolute_url(self):
        return reverse("movies:actor_detail", kwargs={"actor_id": self.id})


class Director(AbstractPerson):
    """Режиссеры."""

    class Meta(AbstractPerson.Meta):
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"

    def get_absolute_url(self):
        return reverse(
            "movies:director_detail",
            kwargs={"director_id": self.id}
        )


class Category(AbstractCategory):
    """Категории фильмов."""

    slug = models.SlugField("Идентификатор", max_length=100, unique=True)

    class Meta(AbstractCategory.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse("movies:category_detail", kwargs={"slug": self.slug})


class Genre(AbstractCategory):
    """Жанры фильмов."""
    slug = models.SlugField("Идентификатор", max_length=100, unique=True)

    class Meta(AbstractCategory.Meta):
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def get_absolute_url(self):
        return reverse("movies:genre_detail", kwargs={"genre_slug": self.slug})


class Movie(models.Model):
    """Фильмы."""

    name = models.CharField("Название", max_length=100, db_index=True)
    description = models.TextField("Описание", blank=True, null=True)
    release_year = models.PositiveSmallIntegerField(
        "Год выпуска",
        validators=[
            MaxValueValidator(
                timezone.now().year,
                "Год выпуска не может быть больше нынешнего!"
            )
        ],
    )
    poster = models.ImageField(
        "Постер", upload_to="movies/%Y/%m/%d", null=True, blank=True
    )
    category = models.ForeignKey(
        to="Category", on_delete=models.SET_DEFAULT, default="Без категории",
        null=True, blank=True
    )
    genres = models.ManyToManyField(
        to="Genre", related_name="genre_movies", verbose_name="Жанры фильма"
    )
    countries = models.ManyToManyField(
        to="Country", related_name="country_movies",
        verbose_name="Страны производства"
    )
    actors = models.ManyToManyField(
        to="Actor", related_name="actor_movies",
        verbose_name="Актеры фильма"
    )
    directors = models.ManyToManyField(
        to="Director", related_name="director_movies",
        verbose_name="Режиссеры фильма"
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ['name', 'release_year']

    def __str__(self):
        return f"{self.name}({self.release_year})"

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"movies:movie_id": self.id})
