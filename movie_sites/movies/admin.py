from django.contrib import admin

from .models import (
    Person,
    Country,
    Movie,
    Genre,
    Category,
    Comment,
    MovieActor,
    Rating,
    LikeDislike,
    Bookmark,
    ContentType
)


admin.site.register(Person)
admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(LikeDislike)
admin.site.register(Bookmark)
admin.site.register(ContentType)


class ActorInline(admin.TabularInline):
    model = MovieActor


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = (ActorInline,)
