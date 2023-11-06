from django.urls import path
from .views import (
    CategoryCreateView,
    CategoryListView,
    PersonListView,
    PersonCreateView,
    PersonDetailView,
    GenreListView,
    GenreDetailView,
    GenreCreateView,
    CountryListView,
    CountryDetailView,
    CountryCreateView,
    MovieListView,
    MovieDetailView,
    MovieCreateView,
    AddComment,
    AddRating,
    LikeDislikeView,
    MovieCategoriesView,
    AddBookmarkView,
    BookmarkListView
)
from .models import Comment, Person, Movie

app_name = "movies"

urlpatterns = [
    path("", MovieListView.as_view(), name="index"),
    path(
        "movie/<int:movie_id>/",
        MovieDetailView.as_view(),
        name="movie_detail"
    ),
    path("movie/create/", MovieCreateView.as_view(), name="movie_create"),
    path("persons/", PersonListView.as_view(), name="persons"),
    path("person/create/", PersonCreateView.as_view(), name="person_create"),
    path(
        "person/<int:person_id>/",
        PersonDetailView.as_view(),
        name="person_detail"
    ),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path(
        "category/<slug:category_slug>",
        MovieCategoriesView.as_view(),
        name="movie_categories"
    ),
    path(
        "category/create/",
        CategoryCreateView.as_view(),
        name="category_create"
    ),
    path("genres/", GenreListView.as_view(), name="genre_list"),
    path("genre/<slug:slug>", GenreDetailView.as_view(), name="genre_detail"),
    path("genre/create/", GenreCreateView.as_view(), name="genre_create"),
    path("countries/", CountryListView.as_view(), name="country_list"),
    path(
        "country/<int:country_id>",
        CountryDetailView.as_view(),
        name="country_detail"
    ),
    path(
        "country/create/",
        CountryCreateView.as_view(),
        name="country_create"
    ),
    path("comment/<int:pk>/", AddComment.as_view(), name="add_comment"),
    path("add_rating/", AddRating.as_view(), name="add_rating"),
    path(
        "comment/<int:pk>/like_dislike/<str:vote>",
        LikeDislikeView.as_view(model=Comment),
        name="vote_comment"
    ),
    path(
        "person/<int:pk>/like_dislike/<str:vote>",
        LikeDislikeView.as_view(model=Person),
        name="vote_person"
    ),
    path(
        "person/<int:pk>/bookmark",
        AddBookmarkView.as_view(model=Person),
        name="add_bookmark_person"
        ),
    path(
        "movie/<int:pk>/bookmark",
        AddBookmarkView.as_view(model=Movie),
        name="add_bookmark_movie"
        ),
    path(
        "bookmark/persons",
        BookmarkListView.as_view(
            model=Person, template_name="movies/person_list.html"),
        name="bookmark_persons"
    ),
    path(
        "bookmark/movies",
        BookmarkListView.as_view(
            model=Movie, template_name="movies/movies.html"),
        name="bookmark_movies"
    ),
]
