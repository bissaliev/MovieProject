from django.urls import path
from .views import (
    CategoryCreateView,
    CategoryDetailView,
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
    SearchMovie,
    AddComment,
    AddRating,
    SearchPerson,
    PersonCategoryView
)


app_name = "movies"

urlpatterns = [
    path("", MovieListView.as_view(), name="index"),
    path("search/", SearchMovie.as_view(), name="search"),
    path("search_person/", SearchPerson.as_view(), name="search_person"),
    path(
        "movie/<int:movie_id>/",
        MovieDetailView.as_view(),
        name="movie_detail"
    ),
    path("movie/create/", MovieCreateView.as_view(), name="movie_create"),
    path("persons/", PersonListView.as_view(), name="persons"),
    path("person_cat/", PersonCategoryView.as_view(), name="person_category"),
    path("person/create/", PersonCreateView.as_view(), name="person_create"),
    path(
        "person/<int:person_id>/",
        PersonDetailView.as_view(),
        name="person_detail"
    ),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path(
        "category/<slug:slug>",
        CategoryDetailView.as_view(),
        name="category_detail"
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
    path("add_rating/", AddRating.as_view(), name="add_rating")
]
