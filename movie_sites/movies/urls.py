from django.urls import path

from .models import Comment, Movie, Person
from .views import (
    AddBookmarkView, AddComment, AddRating, BookmarkMovieListView,
    BookmarkPersonListView, LikeDislikeView, MovieCategoriesView,
    MovieCreateView, MovieDetailView, MovieListView, MovieSearchView,
    PersonCreateView, PersonDetailView, PersonListView,
)

app_name = "movies"

urlpatterns = [
    path("", MovieListView.as_view(), name="index"),
    path("movie/<int:movie_id>/", MovieDetailView.as_view(), name="movie_detail"),
    path("movie/create/", MovieCreateView.as_view(), name="movie_create"),
    path("persons/", PersonListView.as_view(), name="persons"),
    path("person/create/", PersonCreateView.as_view(), name="person_create"),
    path("person/<int:person_id>/", PersonDetailView.as_view(), name="person_detail"),
    path(
        "category/<slug:category_slug>",
        MovieCategoriesView.as_view(),
        name="movie_categories",
    ),
    path("comment/<int:pk>/", AddComment.as_view(), name="add_comment"),
    path("add_rating/", AddRating.as_view(), name="add_rating"),
    path(
        "comment/<int:pk>/like_dislike/<str:vote>",
        LikeDislikeView.as_view(model=Comment),
        name="vote_comment",
    ),
    path(
        "person/<int:pk>/like_dislike/<str:vote>",
        LikeDislikeView.as_view(model=Person),
        name="vote_person",
    ),
    path(
        "person/<int:pk>/bookmark",
        AddBookmarkView.as_view(model=Person),
        name="add_bookmark_person",
    ),
    path(
        "movie/<int:pk>/bookmark",
        AddBookmarkView.as_view(model=Movie),
        name="add_bookmark_movie",
    ),
    path(
        "bookmark/persons",
        BookmarkPersonListView.as_view(),
        name="bookmark_persons",
    ),
    path(
        "bookmark/movies",
        BookmarkMovieListView.as_view(),
        name="bookmark_movies",
    ),
    path("search/", MovieSearchView.as_view(), name="movie_search"),
]
