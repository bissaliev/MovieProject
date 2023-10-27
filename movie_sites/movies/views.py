from collections.abc import Sequence
from typing import Any
from django.contrib import messages
from django.db.models import Avg
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import (
    Person,
    Category,
    Genre,
    Country,
    Movie,
    Rating,
    LikeDislike,
    Bookmark
)
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
from .utils import get_ip
from .filters import FilterOrderPersonMixin, FilterOrderMovieMixin, FilterOrderMultipleMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.views.generic.base import View, TemplateView


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


class PersonListView(FilterOrderPersonMixin, ListView):
    """Список персон."""
    model = Person
    template_name = "movies/person_list.html"
    paginate_by = 6
    extra_context = {"title": "Персоны"}


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


class MovieListView(FilterOrderMovieMixin, ListView):
    """Список фильмов."""
    model = Movie
    template_name = "movies/movies.html"
    paginate_by = 6
    extra_context = {"title": "Фильмы"}


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
    template_name = "movies/movies.html"
    slug_url_kwarg = "category_slug"
    extra_context = {"title": "Категория"}


class MovieCategoriesView(FilterOrderMovieMixin, ListView):
    model = Movie
    template_name = "movies/movies.html"
    paginate_by = 6

    def get_queryset(self) -> QuerySet[Any]:
        category_slug = self.kwargs["category_slug"]
        return super().get_queryset().filter(category__slug=category_slug)


class CategoryCreateView(CreateView):
    """Создание категории."""
    form_class = CategoryForm
    template_name = "movies/category_create.html"
    success_url = reverse_lazy("movies:category_list")
    extra_context = {"title": "Создание новой категории"}


class LikeDislikeView(View):
    model = None

    def get(self, request, pk, vote):
        votes = {
            "1": "like",
            "-1": "dislike"
        }
        obj = self.model.objects.get(pk=pk)
        content_type = ContentType.objects.get_for_model(obj)
        likedislike, created = LikeDislike.objects.get_or_create(
            user=request.user, content_type=content_type, object_id=obj.id
        )
        if not created and likedislike.vote == int(vote):
            likedislike.delete()
            messages.success(request, f"{votes[vote]} удален")
        else:
            likedislike.vote = vote
            likedislike.save()
            messages.success(request, f"{votes[vote]} создан")
        return redirect(request.META.get("HTTP_REFERER", "/"))


class AddBookmarkView(View):
    model = None

    def get(self, request, pk):
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(self.model),
            object_id=pk
        )
        if not created:
            bookmark.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))


class BookmarkListView(FilterOrderMultipleMixin, ListView):
    model = None
    template_name = None
    paginate_by = 6

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(bookmarks__user=self.request.user)


class BookmarkMainListView(TemplateView):
    models = [Person, Movie]
    template_name = "movies/bookmark_list.html"

    def get(self, request, *args, **kwargs):
        bookmarks = {}
        for model in self.models:
            bookmarks[model.__name__.lower()] = model.objects.filter(
                bookmarks__user=request.user
            )[:5]

        context = self.get_context_data(**kwargs)
        context["bookmarks"] = bookmarks
        return self.render_to_response(context)
