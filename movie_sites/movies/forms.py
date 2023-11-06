from django import forms
from .models import (
    Person,
    Genre,
    Country,
    Movie,
    Comment,
    MovieActor,
    Rating,
)


class CommentForm(forms.ModelForm):
    """Форма для комментариев."""

    class Meta:
        model = Comment
        fields = ("name", "email", "text")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={"class": "form-control border"})
        }


class PersonForm(forms.ModelForm):
    """Форма для создания персоны."""

    class Meta:
        model = Person
        fields = "__all__"


class MovieForm(forms.ModelForm):
    """Форма для создания фильма."""
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
    """Форма для отображения полей для фильтрации, сортировки и поиску фильмов."""

    CHOICE_YEARS = [
        (i, i) for i in sorted(list(set(
            Movie.objects.values_list("release_year", flat=True)
        )))
    ]
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
    search = forms.CharField(required=False, label="Поиск")
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
    filter_years = forms.MultipleChoiceField(
        choices=CHOICE_YEARS, widget=forms.CheckboxSelectMultiple,
        label="Года"
    )
    filter_rating = forms.MultipleChoiceField(
        choices=Rating.RATING_CHOICES, widget=forms.CheckboxSelectMultiple,
        label="Рейтинг"
    )

    class Meta:
        fields = (
            "name", "release_year", "rating", "genres", "years", "rating",
            "filter_countries", "search"
        )


MovieFormSet = forms.inlineformset_factory(
    Movie, MovieActor, form=MovieActorForm
)


class FilterPersonForm(forms.Form):
    """Форма для отображения полей для фильтрации, сортировки и поиску персон."""

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
    search = forms.CharField(required=False, label="Поиск")
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
