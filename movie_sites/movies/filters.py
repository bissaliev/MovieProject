from django.db.models import Q

from .models import Person, MovieActor
from .forms import FilterPersonForm, FilterMovieForm


class FilterOrderPersonMixin:
    """
    Миксин для фильтрации персон по профилю(режиссер или актер), полу;
    поиск персон по фамилии и имени;
    сортировка по имени(А-Я, Я-А), по дате рождения(на убывание и возрастание).
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = FilterPersonForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        actor_ids = MovieActor.objects.values_list("actor_id", flat=True)
        search = self.request.GET.get("search")
        profile = self.request.GET.get("profile")
        gender = self.request.GET.get("gender")
        sort = self.request.GET.getlist("sort")
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        if profile:
            if profile == "actors":
                queryset = queryset.filter(id__in=actor_ids)
            else:
                queryset = queryset.exclude(id__in=actor_ids)
        if gender:
            return queryset.filter(gender=gender)
        return queryset.order_by(*sort)


class FilterOrderMovieMixin:
    """
    Миксин для фильтрации по жанрам, рейтингу на сайте, странам, году создания;
    поиск по названию;
    сортировка по названию(А-Я, Я-А), рейтингу(На убывание и возрастание),
    году производства(На возрастание и убывание).
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = FilterMovieForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_genres = self.request.GET.getlist("filter_genres")
        filter_rating = self.request.GET.get("filter_rating")
        filter_countries = self.request.GET.getlist("filter_countries")
        start_year = self.request.GET.get("start_year")
        end_year = self.request.GET.get("end_year")
        if filter_genres:
            queryset = queryset.filter(genres__id__in=filter_genres)
        if filter_rating:
            queryset = queryset.filter(rating__gte=filter_rating)
        if filter_countries:
            queryset = queryset.filter(countries__id__in=filter_countries)
        if start_year and end_year:
            queryset = queryset.filter(
                release_year__gte=start_year,
                release_year__lte=end_year
            )
        sort = self.request.GET.getlist("sort")
        return queryset.order_by(*sort)


class FilterOrderMultipleMixin:
    """
    Миксин для динамического определения фильтра для персон или фильмов
    (FilterOrderPersonMixin, FilterOrderMovieMixin) для класса представления
    BookmarkListView.
    """

    def get(self, request, *args, **kwargs):
        if self.model == Person:
            self.__class__ = type(
                self.__class__.__name__,
                (FilterOrderPersonMixin, self.__class__), {}
            )
        else:
            self.__class__ = type(
                self.__class__.__name__,
                (FilterOrderMovieMixin, self.__class__), {}
            )
        return super().get(request, *args, **kwargs)
