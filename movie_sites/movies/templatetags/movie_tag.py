from django import template
from ..models import Category, Movie, ContentType, LikeDislike

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_status_vote(obj, user):
    content_type = ContentType.objects.get_for_model(obj)
    try:
        likedislike = LikeDislike.objects.get(
            user=user,
            content_type=content_type,
            object_id=obj.id
        )
        vote = likedislike.vote
    except LikeDislike.DoesNotExist:
        vote = None
    return vote


@register.inclusion_tag("movies/tags/last_movies.html")
def get_last_movies(count=5):
    movies = Movie.objects.all().order_by("-id")[:count]
    return {"last_movies": movies}
