from django import forms
from .models import (
    Person,
    Category,
    Genre,
    Country,
    Movie,
    Comment,
    MovieActor,
    Rating,
)


class CommentForm(forms.ModelForm):
    """Форма комментариев."""
    # captcha = ReCaptchaField()

    class Meta:
        model = Comment
        fields = ("name", "email", "text")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={"class": "form-control border"})
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = "__all__"


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = "__all__"


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"
        exclude = ("actors",)


class MovieActorForm(forms.ModelForm):
    class Meta:
        model = MovieActor
        fields = "__all__"


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ("score",)


class FilterMovieForm(forms.Form):
    CHOICE_YEARS = [
        (i, i) for i in sorted(list(set(
            Movie.objects.values_list("release_year", flat=True)
        )))
    ]
    NAME_SORT_CHOICES = (
        (None, "не выбрано"),
        ("name", "А-Я"),
        ("-name", "Я-А")
    )
    YEAR_SORT_CHOICES = (
        (None, "не выбрано"),
        ("release_year", "На возрастание"),
        ("-release_year", "На убывание")
    )
    RATING_SORT_CHOICES = (
        (None, "не выбрано"),
        ("rating", "На возрастание"),
        ("-rating", "На убывание")
    )
    name = forms.ChoiceField(
        choices=NAME_SORT_CHOICES, label="По заголовку", required=False
    )
    release_year = forms.ChoiceField(
        choices=YEAR_SORT_CHOICES, label="По годам", required=False
    )
    rating = forms.ChoiceField(
        choices=RATING_SORT_CHOICES, label="По рейтингу", required=False
    )
    filter_genres = forms.ModelChoiceField(
        queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple,
        label="Жанры"
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
            "name", "release_year", "rating", "genres", "years", "rating"
        )


MovieFormSet = forms.inlineformset_factory(
    Movie, MovieActor, form=MovieActorForm
)


class ActorDirectorForm(forms.Form):
    CHOICE_PERSON_PROFILE = [
        ("actors", "Актеры"),
        ("directors", "Режиссеры"),
    ]
    profile = forms.ChoiceField(
        choices=CHOICE_PERSON_PROFILE,
        label="Категория",
        widget=forms.CheckboxSelectMultiple
    )
    gender = forms.ChoiceField(
        choices=Person.GENDER_CHOICES,
        label="Пол",
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
