from abc import ABC, abstractclassmethod

from django.db.models import Q

from .forms import FilterMovieForm, FilterPersonForm
from .models import MovieActor


class FilterBaseMixin(ABC):
    """Базовый фильтр-миксин."""

    filter_form = None

    @abstractclassmethod
    def get_filtered_qs(self, qs):
        """
        Метод который нужно определить в дочерних классах для построения
        логики фильтрации объектов. Метод должен принимать объект QuerySet
        и возвращать отфильтрованный QuerySet.
        """
        pass

    @abstractclassmethod
    def get_mixin_context_data(self, **kwargs):
        """
        Метод который нужно определить в дочерних классах для построения
        логики фильтрации объектов. Метод должен возвращать словарь который
        должен быть включен в контекст.
        """
        pass

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст форму для фильтрации объектов и словарь,
        который является результатов метода 'get_mixin_context_data'.
        """
        print(self.request.GET)
        context = {
            "filter_form": self.filter_form(self.request.GET)
        }
        context |= self.get_mixin_context_data()
        context |= kwargs
        return super().get_context_data(**context)

    def get_queryset(self):
        """Возвращаем окончательный QuerySet."""
        return self.get_sorted_qs(self.get_filtered_qs(super().get_queryset()))

    def get_sorted_qs(self, qs):
        """Метод принимает queryset и отдает отсортированный queryset."""
        return qs.order_by(*self.request.GET.getlist("sort"))


class FilterOrderPersonMixin(FilterBaseMixin):
    """
    Класс для фильтрации персон по профилю(режиссер или актер), полу;
    поиск персон по фамилии и имени; Сортировка по имени(А-Я, Я-А).
    """

    filter_form = FilterPersonForm

    def get_filtered_qs(self, qs):
        """Метод принимает queryset и отдает отфильтрованный queryset;
        Фильтрация производится по полям: Пол, Режиссеры и Актеры.
        Осуществляется поиск по Фамилии и Имени
        """
        actor_ids = MovieActor.objects.values_list("actor_id", flat=True)
        search = self.request.GET.get("search")
        profile = self.request.GET.get("profile")
        gender = self.request.GET.get("gender")
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        if profile:
            if profile == "actors":
                qs = qs.filter(id__in=actor_ids)
            else:
                qs = qs.exclude(id__in=actor_ids)
        if gender:
            qs = qs.filter(gender=gender)
        return qs

    def get_mixin_context_data(self, **kwargs):
        """
        Добавляем в контекст переменные 'current_profile', 'current_gender'
        для отображения в шаблоне выбранных опций фильтрации в предыдущем
        запросе.
        """
        return {
            "current_profile": self.request.GET.getlist("profile"),
            "current_gender": self.request.GET.get("gender"),
        }


class FilterOrderMovieMixin(FilterBaseMixin):
    """
    Класс для фильтрации фильмов по жанрам, рейтингу на сайте, странам,
    году создания; Сортировка по названию(А-Я, Я-А),
    рейтингу(На убывание и возрастание), году производства(На возрастание
    и убывание).
    """

    filter_form = FilterMovieForm

    def get_filtered_qs(self, qs):
        """Метод принимает queryset и отдает отфильтрованный queryset;
        Фильтрация производится по полям: Жанры, Рейтинг, Страны,
        Год производства.
        """

        genres = self.request.GET.getlist("genres")
        rating = self.request.GET.get("rating")
        countries = self.request.GET.getlist("countries")
        start_year = self.request.GET.get("start_year")
        end_year = self.request.GET.get("end_year")
        if genres:
            qs = qs.filter(genres__id__in=genres)
        if rating:
            qs = qs.filter(rating__gte=rating)
        if countries:
            qs = qs.filter(countries__id__in=countries)
        if start_year and end_year:
            qs = qs.filter(release_year__range=(start_year, end_year))
        return qs

    def get_mixin_context_data(self, **kwargs):
        """
        Добавляем в контекст переменные 'current_genre', 'current_countries'
        для отображения в шаблоне выбранных опций фильтрации в предыдущем
        запросе.
        """
        context = {}
        context["current_genre"] = [
            int(i) for i in self.request.GET.getlist("genres")
        ]
        context["current_countries"] = [
            int(i) for i in self.request.GET.getlist("countries")
        ]
        return context
