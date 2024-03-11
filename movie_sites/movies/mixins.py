from django.views.generic import ListView

from .filters import FilterOrderMovieMixin, FilterOrderPersonMixin
from .models import Movie, Person


class BaseMovieListMixin(FilterOrderMovieMixin, ListView):
    """
    Класс-миксин наследуется от класса ListView и
    FilterOrderMovieMixin(фильтрация фильмов).
    """
    model = Movie
    template_name = "movies/movies.html"
    paginate_by = 8
    extra_context = {"title": "Фильмы"}

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст переменные 'current_genre', 'current_countries'
        для отображения в шаблоне выбранных опций фильтрации в предыдущем
        запросе.
        """
        context = super().get_context_data(**kwargs)
        context["current_genre"] = [
            int(i) for i in self.request.GET.getlist("genres")]
        context["current_countries"] = [
            int(i) for i in self.request.GET.getlist("countries")
        ]
        return context


class BasePersonListMixin(FilterOrderPersonMixin, ListView):
    """
    Класс-миксин наследуется от класса ListView и
    FilterOrderPersonMixin(фильтрация персон).
    """
    model = Person
    template_name = "movies/person_list.html"
    paginate_by = 8
    extra_context = {"title": "Персоны"}

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст переменные 'current_profile', 'current_gender'
        для отображения в шаблоне выбранных опций фильтрации в предыдущем
        запросе.
        """
        context = super().get_context_data(**kwargs)
        current_profile = self.request.GET.getlist("profile")
        current_gender = self.request.GET.get("gender")
        context["current_profile"] = current_profile
        context["current_gender"] = current_gender
        print(current_gender)
        return context
