from django.contrib import admin

from .models import Actor, Director, Country, Movie, Genre, Category


admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Country)
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Category)
