import json

from typing import Any
from django.core.management.base import BaseCommand
from django.core.files import File
from ...models import Movie, Country, Genre, Category


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        count = 0
        category = Category.objects.get(name="Фильмы", slug="film")
        with open("/home/bissalievok/Dev/parser/film_popular_foreign_short.json", "r") as film:
            info_film = json.load(film)

        for film in info_film:
            name = film["Название"]
            year = film["Год"]
            countries = film["Страна"]
            genres = film["Жанры"]
            movie, _ = Movie.objects.get_or_create(name=name, release_year=year)
            for country in countries:
                c, _ = Country.objects.get_or_create(name=country.strip().title())
                movie.countries.add(c)
            for genre in genres:
                count += 1
                g, created = Genre.objects.get_or_create(name=genre.strip().title())
                if created:
                    g.slug = f"slug_{count}"
                    g.save()
                movie.genres.add(g)
                movie.category = category
            movie.save()

            if not movie.poster:
                with open(f"/home/bissalievok/Dev/parser/poster_popular/{name.replace(' ', '_')}.jpeg", "rb") as img:
                    poster = img
                    movie, _ = Movie.objects.get_or_create(name=name, release_year=year)
                    movie.poster.save(f"{name.replace(' ', '_')}.jpeg", File(poster))
