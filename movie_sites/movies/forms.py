import datetime as dt

from django import forms
from .models import (
    Person,
    Genre,
    Country,
    Movie,
    Comment,
    MovieActor,
    Rating,
    Category
)

year = dt.datetime.now().year


class CommentForm(forms.ModelForm):
    """Форма для комментариев."""

    class Meta:
        model = Comment
        fields = ("name", "email", "text")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border", "placeholder": "Имя"}),
            "email": forms.EmailInput(attrs={"class": "form-control border", "placeholder": "Email"}),
            "text": forms.Textarea(attrs={"class": "form-control border", "placeholder": "Ваш комментарий"})
        }


class PersonForm(forms.ModelForm):
    """Форма для создания персоны."""
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Имя"}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Фамилия"}))
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Введите текс биографии", "rows": 18})
    )

    class Meta:
        model = Person
        fields = "__all__"


class MovieForm(forms.ModelForm):
    """Форма для создания фильма."""

    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Название фильма"})
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Напишите описание фильма"})
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.SelectMultiple,
        label="Жанры"
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select,
        label="Категория",
        empty_label="Выберете категорию"
    )

    class Meta:
        model = Movie
        fields = "__all__"
        exclude = ("actors",)


class MovieActorForm(forms.ModelForm):
    class Meta:
        model = MovieActor
        fields = "__all__"


class RatingForm(forms.ModelForm):
    """Форма для добавление рейтинга на определенный фильм."""

    class Meta:
        model = Rating
        fields = ("score",)


class FilterMovieForm(forms.Form):
    """
    Форма для отображения полей для фильтрации, сортировки и поиску фильмов.
    """

    CHOICE_YEARS = [(i, i) for i in range(year, year-100, -1)]

    SORT_CHOICES = (
        ("по заголовку", (
            ("name", "А-Я"),
            ("-name", "Я-А")
        )),
        ("по годам", (
            ("release_year", "На возрастание"),
            ("-release_year", "На убывание")
        )),
        ("по рейтингу", (
            ("rating", "На возрастание"),
            ("-rating", "На убывание")
        )),
    )
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        widget=forms.Select,
        label="Сортировать по:",
        required=False,
    )
    filter_genres = forms.ModelChoiceField(
        queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple,
        label="Жанры"
    )
    filter_countries = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Страны"
    )
    filter_rating = forms.MultipleChoiceField(
        choices=Rating.RATING_CHOICES, widget=forms.CheckboxSelectMultiple,
        label="Рейтинг"
    )
    start_year = forms.ChoiceField(choices=reversed(CHOICE_YEARS), initial=1950)
    end_year = forms.ChoiceField(initial=year, choices=CHOICE_YEARS)

    class Meta:
        fields = (
            "name", "release_year", "rating", "genres", "rating",
            "filter_countries", "start_year", "end_year"
        )


class FilterPersonForm(forms.Form):
    """
    Форма для отображения полей для фильтрации, сортировки и поиску персон.
    """

    PERSON_PROFILE_CHOICES = [
        ("actors", "Актеры"),
        ("directors", "Режиссеры"),
    ]
    SORT_CHOICES = [
        ("по имени", (("first_name", "А-Я"), ("-first_name", "Я-А"))),
        ("по фамилии", (("last_name", "А-Я"), ("-last_name", "Я-А"))),
        ("по дате рождения", (
            ("birthdate", "На возрастание"), ("-birthdate", "На убывание")
        ))
    ]
    search = forms.CharField(
        required=False,
        label="Поиск",
        widget=forms.TextInput(attrs={"placeholder": "Поиск"})
    )
    profile = forms.ChoiceField(
        choices=PERSON_PROFILE_CHOICES,
        label="Категория",
        widget=forms.CheckboxSelectMultiple
    )
    gender = forms.ChoiceField(
        choices=Person.GENDER_CHOICES,
        label="Пол",
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    sort = forms.ChoiceField(
        choices=SORT_CHOICES, widget=forms.Select, label="Сортировать по:"
    )

    class Meta:
        fields = ("search", "profile", "gender", "sort")
