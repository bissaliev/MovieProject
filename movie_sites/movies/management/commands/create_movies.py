from typing import Any
from django.core.management.base import BaseCommand
from django.core.files import File
from ...models import Movie

countries = ["США", " Канада"]
genres = ["драма", " криминал", " триллер"]


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        name = "Бегущий по лезвию"
        year = 1982
        poster = open("/home/bissalievok/Dev/parser/poster_popular/Бегущий_по_лезвию.jpeg", "rb")
        movie = Movie.objects.create(name=name, release_year=year)
        movie.poster.save("Бегущий_по_лезвию.jpeg", File(poster))
        poster.close()
