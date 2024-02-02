from rest_framework.viewsets import ReadOnlyModelViewSet

from movies.models import Movie, Person
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    PersonListSerializer,
    PersonDetailSerializer
)


class MovieViewSet(ReadOnlyModelViewSet):
    """Вьюсет для фильмов."""

    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return super().get_serializer_class()
        return MovieDetailSerializer


class PersonViewSet(ReadOnlyModelViewSet):
    """Вьюсет для персон."""
    queryset = Person.objects.all()
    serializer_class = PersonListSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return super().get_serializer_class()
        return PersonDetailSerializer
