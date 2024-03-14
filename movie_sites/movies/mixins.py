from django.views.generic import ListView

from .filters import FilterOrderMovieMixin, FilterOrderPersonMixin
from .models import Movie, Person

# Переменная определяет кол-во объектов на странице
QUANTITY_PER_PAGE: int = 8


class BaseMovieListMixin(FilterOrderMovieMixin, ListView):
    """
    Класс-миксин наследуется от класса ListView и
    FilterOrderMovieMixin(фильтрация фильмов).
    """
    model = Movie
    template_name = "movies/movies.html"
    paginate_by = QUANTITY_PER_PAGE
    extra_context = {"title": "Фильмы"}


class BasePersonListMixin(FilterOrderPersonMixin, ListView):
    """
    Класс-миксин наследуется от класса ListView и
    FilterOrderPersonMixin(фильтрация персон).
    """
    model = Person
    template_name = "movies/person_list.html"
    paginate_by = QUANTITY_PER_PAGE
    extra_context = {"title": "Персоны"}
