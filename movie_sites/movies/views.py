from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Q
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.base import View

from .filters import FilterOrderMovieMixin, FilterOrderPersonMixin
from .forms import (
    CommentForm, MovieActorForm, MovieForm, PersonForm, RatingForm,
)
from .models import Bookmark, LikeDislike, Movie, MovieActor, Person, Rating
from .utils import get_ip


class MovieListView(FilterOrderMovieMixin, ListView):
    """Класс-представление для вывода списка всех фильмов с пагинацией."""

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
            int(i) for i in self.request.GET.getlist("countries")]
        return context


class MovieDetailView(DetailView):
    """Класс-представление для вывода определенного фильма по 'id'."""

    model = Movie
    template_name = "movies/movie_detail.html"
    pk_url_kwarg = "movie_id"

    def get_context_data(self, **kwargs):
        """
        Добавление формы 'RatingForm' с полем 'score' для оценки пользователем
        текущего фильма. Поле 'ip' определяется из request.
        Если пользователь уже оценил фильм, то выводит его предыдущую оценку.
        """

        context = super().get_context_data(**kwargs)
        context["rating_form"] = RatingForm()
        context["form"] = CommentForm()
        return context


class MovieSearchView(FilterOrderMovieMixin, ListView):
    """Класс-представления для поиска фильма по названию."""

    model = Movie
    template_name = "movies/movies.html"
    paginate_by = 8

    def get_queryset(self):
        search = self.request.GET.get("s")
        if search:
            return super().get_queryset().filter(name__icontains=search)
        return super().get_queryset()


class SearchView(FilterOrderMovieMixin, View):
    def get(self, request):
        s = request.GET.get("s")
        search_selection = request.GET.get("search_selection")
        if s:
            if search_selection == 1:
                qs = Movie.objects.filter(name__icontains=s)
                return render(request, "movies/movies.html", {"object_list": qs})
            qs = Person.objects.filter(
                Q(first_name__icontains=s) | Q(last_name__icontains=s)
            )
            return render(request, "movies/person_list.html", {"object_list": qs})


class PersonSearchView(ListView): # не активна
    """класс представление для поиска персон."""

    model = Person
    template_name = "movies/person_list.html"
    paginate_by = 8

    def get_queryset(self):
        search = self.request.GET.get("s")
        return Person.objects.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search)
        )


class MovieCreateView(CreateView):  # добавить функционал чтобы добавлять мог только администратор
    """Создание нового фильма."""

    form_class = MovieForm
    template_name = "movies/movie_create.html"
    extra_context = {"title": "Создание нового фильма"}
    formset = inlineformset_factory(
        Movie, MovieActor, form=MovieActorForm, extra=2)

    def get_context_data(self, **kwargs):
        """Добавляем в контекст formset."""
        context = super().get_context_data(**kwargs)
        context["movie_formset"] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.get_form_class())
        movie_formset = self.formset(
            request.POST or None, request.FILES or None)

        if (form.is_valid()) and (movie_formset.is_valid()):
            return self.form_valid(form, movie_formset)

        return self.form_invalid(form, movie_formset)

    def form_valid(self, form, movie_formset):
        """
        Если данные проходят валидацию, то мы сохраняем сначала объект модели
        Movie; Затем связываем объект Movie и объект Person через промежуточную
        модель MovieActor.
        """

        self.object = form.save()
        movie_formset.instance = self.object
        movie_formset.save()
        return super(MovieCreateView, self).form_valid(form)

    def form_invalid(self, form, movie_formset):
        """
        Если данные не проходят валидацию возвращаем введенные данные
        на страницу пользователя.
        """

        return self.render_to_response(
            self.get_context_data(form=form, movie_formset=movie_formset)
        )


class PersonListView(FilterOrderPersonMixin, ListView):
    """Возвращает список персон."""
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


class PersonCreateView(CreateView):
    """Создание персоны."""
    form_class = PersonForm
    template_name = "movies/person_create.html"
    success_url = reverse_lazy("movies:persons")
    extra_context = {"title": "Создание нового актера"}


class PersonDetailView(DetailView):
    """Возвращает определенную по id персону."""
    model = Person
    template_name = "movies/person_detail.html"
    extra_context = {"title": "Детальная информация"}
    pk_url_kwarg = "person_id"


class AddComment(View):
    """Добавление комментария."""

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
    """Добавление рейтинга фильму."""

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


class MovieCategoriesView(FilterOrderMovieMixin, ListView):
    """Возвращает список фильмов по определенной категории."""
    model = Movie
    template_name = "movies/movies.html"
    paginate_by = 8

    def get_queryset(self):
        category_slug = self.kwargs["category_slug"]
        return super().get_queryset().filter(category__slug=category_slug)


class LikeDislikeView(View):
    """
    Создание лайков и дизлайков на определенный контент,
    а также их удаление.
    """
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
    """Добавление закладки на определенный контент, а также её удаление."""
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


class BookmarkMovieListView(FilterOrderMovieMixin, ListView):
    """
    Возвращает список фильмов, находящихся в закладках у определенного
    авторизированного пользователя.
    """

    model = Movie
    template_name = "movies/movies.html"
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().filter(bookmarks__user=self.request.user)


class BookmarkPersonListView(FilterOrderPersonMixin, ListView):
    """
    Возвращает список персон, находящихся в закладках у определенного
    авторизированного пользователя.
    """

    model = Person
    template_name = "movies/person_list.html"
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().filter(bookmarks__user=self.request.user)
