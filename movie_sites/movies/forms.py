from django import forms
from .models import (
    Person,
    Category,
    Genre,
    Country,
    Movie,
    Comment,
    MovieActor,
    Rating
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
    # CHOICES = [
    #     (1, 1),
    #     (2, 2),
    #     (3, 3),
    #     (4, 4),
    #     (5, 5),
    #     (6, 6),
    #     (7, 7),
    #     (8, 8),
    #     (9, 9),
    #     (10, 10),
    # ]
    # score = forms.ChoiceField(
    #     widget=forms.RadioSelect(), choices=Rating.RATING_CHOICES
    # )

    class Meta:
        model = Rating
        fields = ("score",)


MovieFormSet = forms.inlineformset_factory(
    Movie, MovieActor, form=MovieActorForm
)
