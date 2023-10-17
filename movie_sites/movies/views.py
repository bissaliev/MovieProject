from django.db.models import Q
from django.db.models import Count, Avg
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Person, Category, Genre, Country, Movie, Rating
from .forms import (
    PersonForm,
    CategoryForm,
    GenreForm,
    CountryForm,
    MovieForm,
    CommentForm,
    RatingForm,
    MovieFormSet
)
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
# from django.views.generic.base import View
from django.views import View


def get_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class AddRating(View):
    """Добавление рейтинга."""

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, _ = Rating.objects.update_or_create(
                movie_id=int(request.POST.get("movie")),
                ip=get_ip(request),
                defaults={"score": request.POST.get("score")}
            )
            avg_rating = rating.movie.ratings.values("movie").annotate(avg=Avg("score"))[0].get("avg")
            rating.movie.rating = avg_rating
            rating.movie.save()
            return redirect("movies:movie_detail", request.POST.get("movie"))  # HttpResponse(status=201)
        return HttpResponse(status=400)


class MovieCreateView(CreateView):
    """Создание нового фильма."""

    form_class = MovieForm
    template_name = "movies/movie_create.html"
    success_url = reverse_lazy("movies:index")
    extra_context = {"title": "Создание нового фильма"}

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        movie_formset = MovieFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, movie_formset=movie_formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        movie_formset = MovieFormSet(request.POST, request.FILES)
        if (form.is_valid()) and (movie_formset.is_valid()):
            return self.form_valid(form, movie_formset)
        else:
            return self.form_invalid(form, movie_formset)

    def form_valid(self, form, movie_formset):
        self.object = form.save()
        movie_formset.instance = self.object
        movie_formset.save()
        return super(MovieCreateView, self).form_valid(form)

    def form_invalid(self, form, movie_formset):
        return self.render_to_response(
            self.get_context_data(form=form, movie_formset=movie_formset)
        )


class AddComment(View):
    """Добавление комментариев."""

    def post(self, request, pk):
        form = CommentForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("major", None):
                form.major_id = int(request.POST.get("major"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class GenreYear:
    """Класс миксин для фильтрации фильмов по жанрам и годам."""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.all().values(
            'release_year'
        ).annotate(Count('release_year'))

    def get_ratings(self):
        return range(1, 11)

    # def get_ratings(self):
    #     return Rating.objects.values("movie").annotate(avr_rating=Avg("score"))


class FilterMovieView(GenreYear, ListView):
    """Фильтрация фильмов по жанрам и годам."""
    template_name = "movies/movies.html"

    def get_queryset(self):
        rating = self.request.GET.get("rating")
        if not rating:
            rating = 0
        queryset = Movie.objects.filter(
            Q(Q(release_year__in=self.request.GET.getlist("release_year")) |
            Q(genres__in=self.request.GET.getlist("genre"))) &
            Q(rating__gte=rating)
        ).distinct()
        # if self.request.GET.get("rating"):
        #     if queryset:
        #         queryset = queryset.filter(rating__gte=self.request.GET.get("rating"))
        #     else:
        #         queryset = Movie.objects.filter(rating__gte=self.request.GET.get("rating"))
        return queryset


class SearchMovie(ListView):
    """Поиск фильмов по названию."""
    template_name = "movies/movies.html"

    def get_queryset(self):
        return Movie.objects.filter(
            name__icontains=self.request.GET.get("search")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search")
        return context


class PersonListView(ListView):
    """Список персон."""
    model = Person
    template_name = "movies/person_list.html"
    extra_context = {"title": "Актеры"}


class PersonCreateView(CreateView):
    """Создание персоны."""
    form_class = PersonForm
    template_name = "movies/person_create.html"
    success_url = reverse_lazy("movies:persons")
    extra_context = {"title": "Создание нового актера"}


class PersonDetailView(DetailView):
    """Персона."""
    model = Person
    template_name = "movies/person_detail.html"
    extra_context = {"title": "Детальная информация"}
    pk_url_kwarg = "person_id"


class CategoryListView(ListView):
    """Список категорий."""
    model = Category
    template_name = "movies/category_list.html"
    extra_context = {"title": "Категории"}


class CategoryDetailView(DetailView):
    """категория."""
    model = Category
    template_name = "movies/category_detail.html"  # "movies/movies.html"
    extra_context = {"title": "Категория"}

    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context["object_list"] = context["object"].movie_set.all()
    #     return context


class CategoryCreateView(CreateView):
    """Создание категории."""
    form_class = CategoryForm
    template_name = "movies/category_create.html"
    success_url = reverse_lazy("movies:category_list")
    extra_context = {"title": "Создание новой категории"}


class GenreListView(ListView):
    """Список жанров."""
    model = Genre
    template_name = "movies/category_list.html"
    extra_context = {"title": "Жанры"}


class GenreDetailView(DetailView):
    """Жанр."""
    model = Genre
    template_name = "movies/category_detail.html"
    extra_context = {"title": "Жанр"}


class GenreCreateView(CreateView):
    """Создание жанра."""
    form_class = GenreForm
    template_name = "movies/category_create.html"
    success_url = reverse_lazy("movies:genre_list")
    extra_context = {"title": "Создание нового жанра"}


class CountryListView(ListView):
    """Список стран."""
    model = Country
    template_name = "movies/category_list.html"
    extra_context = {"title": "Страны"}


class CountryDetailView(DetailView):
    """Страна."""
    model = Country
    template_name = "movies/category_detail.html"
    extra_context = {"title": "Страна"}
    pk_url_kwarg = "country_id"


class CountryCreateView(CreateView):
    """Создание страны."""
    form_class = CountryForm
    template_name = "movies/country_create.html"
    success_url = reverse_lazy("movies:country_list")
    extra_context = {"title": "Создание новой страны"}


class MovieListView(GenreYear, ListView):
    """Список фильмов."""
    model = Movie
    template_name = "movies/movies.html"
    extra_context = {"title": "Фильмы"}

    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context["categories"] = Category.objects.all()
    #     return context


class MovieDetailView(DetailView):
    """Фильм."""
    model = Movie
    template_name = "movies/movie_detail.html"
    extra_context = {"title": "Фильм"}
    pk_url_kwarg = "movie_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object.ratings.filter(ip=get_ip(self.request))
        if instance:
            context["rating_form"] = RatingForm(instance=instance[0])
        else:
            context["rating_form"] = RatingForm()
        context["form"] = CommentForm()
        return context
