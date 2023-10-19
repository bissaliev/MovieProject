from typing import Any
from django.db.models import Avg, Q
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Person, Category, Genre, Country, Movie, Rating, MovieActor, LikeDislike, Comment
from .forms import (
    PersonForm,
    CategoryForm,
    GenreForm,
    CountryForm,
    MovieForm,
    CommentForm,
    RatingForm,
    MovieFormSet,
    FilterMovieForm,
    ActorDirectorForm,
    LikeDislikeForm
)
from .utils import get_ip
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
# from django.views.generic.base import View
from django.views import View


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


class SearchPerson(SearchMovie):
    template_name = "movies/person_list.html"

    def get_queryset(self):
        search = self.request.GET.get("search")
        return Person.objects.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )


class PersonCategoryView(ListView):
    template_name = "movies/person_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["category_form"] = ActorDirectorForm(self.request.GET)
        return context

    def get_queryset(self) -> QuerySet[Any]:
        queryset = Person.objects.all()
        actor_ids = MovieActor.objects.values_list("actor_id", flat=True)
        if self.request.GET.get("profile"):
            if self.request.GET.get("profile") == "actors":
                queryset = queryset.filter(id__in=actor_ids)
            else:
                queryset = queryset.exclude(id__in=actor_ids)
        if self.request.GET.get("gender"):
            return queryset.filter(gender=self.request.GET.get("gender"))
        return queryset


class PersonListView(ListView):
    """Список персон."""
    model = Person
    template_name = "movies/person_list.html"
    extra_context = {"title": "Персоны"}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["category_form"] = ActorDirectorForm()
        return context


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


class MovieListView(ListView):
    """Список фильмов."""
    model = Movie
    template_name = "movies/movies.html"
    extra_context = {"title": "Фильмы"}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["filter_form"] = FilterMovieForm(self.request.GET)
        # context["form_ordering"] = SortMovieForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset().order_by()
        query_filter = []
        filter_genres = self.request.GET.getlist("filter_genres")
        filter_rating = self.request.GET.get("filter_rating")
        filter_years = self.request.GET.getlist("filter_years")
        if filter_genres:
            query_filter.append(queryset.filter(genres__id__in=filter_genres))
        if filter_rating:
            query_filter.append(queryset.filter(rating__gte=filter_rating))
        if filter_years:
            query_filter.append(queryset.filter(release_year__in=filter_years))
        queryset = queryset.intersection(*query_filter)
        sort = []
        name = self.request.GET.get("name")
        release_year = self.request.GET.get("release_year")
        rating = self.request.GET.get("rating")
        if name:
            sort.append(name)
        if release_year:
            sort.append(release_year)
        if rating:
            sort.append(rating)
        queryset = queryset.order_by(*sort)
        return queryset


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
        context["likedislike_form"] = LikeDislikeForm()
        return context


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
            avg_rating = rating.movie.ratings.values(
                "movie"
            ).annotate(avg=Avg("score"))[0].get("avg")
            rating.movie.rating = avg_rating
            rating.movie.save()
            return redirect("movies:movie_detail", request.POST.get("movie"))
        return HttpResponse(status=400)


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


class LikeDislikeView(View):
    model = Comment

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        content_type = ContentType.objects.get_for_model(obj)
        try:
            likedislike = LikeDislike.objects.get(
                content_type=content_type, object_id=obj.id, user=request.user
            )
            if str(likedislike.vote) == self.request.POST.get("vote"):
                print(self.request.POST.get("vote"))
                print(likedislike.vote)
                likedislike.delete()
            else:
                likedislike.vote = self.request.POST.get("vote")
                likedislike.save(update_fields=["vote"])
        except LikeDislike.DoesNotExist:
            obj.votes.create(
                user=request.user, vote=self.request.POST.get("vote")
            )
        return redirect(obj.movie.get_absolute_url())
