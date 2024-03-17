"""Пользовательские теги."""

from django import template

from ..models import (
    Bookmark, Category, ContentType, Country, Genre, LikeDislike, Movie,
)
from ..utils import get_ip

register = template.Library()


@register.simple_tag()
def your_rating(request, object):
    """Определяет ставил ли пользователь оценку фильму."""

    if rating := object.ratings.filter(ip=get_ip(request)):
        return rating[0].score


@register.filter()
def convert_to_number(value):
    """Фильтр конвертирует значение в тип данных int."""
    return int(value)


@register.simple_tag()
def get_genres():
    """
    Функция возвращает Queryset (список все жанров) для вывода их в шаблоне.
    """

    return Genre.objects.all()


@register.simple_tag()
def get_countries():
    """
    Функция возвращает Queryset (список все стран) для вывода их в шаблоне.
    """

    return Country.objects.all()


@register.simple_tag()
def get_categories():
    """
    Функция возвращает Queryset (список все категорий) для вывода их в шаблоне.
    """

    return Category.objects.all()


@register.simple_tag()
def get_status_vote(obj, user):
    """
    Функция извлекает из БД(модель LikeDislike) данные о том поставил ли
    пользователь лайк или дизлайк; Возвращает целое число (1 или -1);
    Если в БД не существует записи, то ловит исключение и возвращает None.
    """

    content_type = ContentType.objects.get_for_model(obj)
    try:
        likedislike = LikeDislike.objects.get(
            user=user,
            content_type=content_type,
            object_id=obj.id
        )
    except LikeDislike.DoesNotExist:
        return None
    return likedislike.vote


@register.simple_tag()
def bookmark_is_exists(obj, user):
    """
    Функция извлекает из БД(модель Bookmark) данные о том, является ли объект
    в списке избранных определенного пользователя.
    """

    content_type = ContentType.objects.get_for_model(obj)
    try:
        Bookmark.objects.get(
            user=user,
            content_type=content_type,
            object_id=obj.id
        )
    except Bookmark.DoesNotExist:
        return False
    return True


@register.inclusion_tag("movies/tags/last_movies.html")
def get_last_movies(count=5):
    """
    Функция извлекает из БД(модель Movie) последние добавленные фильмы на сайт
    для вывод их на страницу. Количество можно задать в шаблоне
    (передается в качестве аргумента функции). По умолчанию 5.
    """

    return {"last_movies": Movie.objects.all().order_by("-id")[:count]}


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Функция для исправления совместимости фильтра и паджинатора;
    Извлекает из kwargs номера страниц и добавляет их в контекстб
    параллельно удаляя старые данные.
    """

    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        print(k)
        del d[k]
    return d.urlencode()


@register.filter
def addclass(field, css):
    """Функция принимает класс стиля CSS и добавляет их полю."""
    return field.as_widget(attrs={'class': css})


@register.filter("add_label_class")
def add_label_class(field, css_class):
    """Функция принимает класс стиля CSS и добавляет label поля."""
    return field.label_tag(attrs={"class": css_class})
