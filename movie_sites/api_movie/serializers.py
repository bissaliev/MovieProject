from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from movies.models import (
    Movie,
    Genre,
    Country,
    Person,
    LikeDislike,
    Rating,
    Comment
)
from movies.utils import get_ip


class FilterCommentListSerializer(serializers.ListSerializer):
    """
    Сериализатор для CommentSerializer, чтобы отфильтровать комментарии,
    которые являются дочерними.
    """
    def to_representation(self, data):
        data = data.filter(major=None)
        return super().to_representation(data)


class CommentChildrenSerializer(serializers.ModelSerializer):
    """
    Вложенный сериализатор для вывода комментариев к определенному комментарию.
    """

    votes = serializers.SerializerMethodField()

    class Meta:
        fields = ("name", "text", "votes")
        model = Comment

    def get_votes(self, obj):
        request = self.context.get("request")
        content_type = ContentType.objects.get_for_model(obj)
        try:
            like = LikeDislike.objects.get(
                user=request.user, content_type=content_type, object_id=obj.id)
        except LikeDislike.DoesNotExist:
            return False
        return like.get_vote_display()


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода комментариев."""

    children = CommentChildrenSerializer(many=True)
    votes = serializers.SerializerMethodField()

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        fields = ("name", "text", "votes", "children")
        model = Comment

    def get_votes(self, obj):
        request = self.context.get("request")
        content_type = ContentType.objects.get_for_model(obj)
        try:
            like = LikeDislike.objects.get(
                user=request.user, content_type=content_type, object_id=obj.id)
        except LikeDislike.DoesNotExist:
            return False
        return like.get_vote_display()


class CountrySerializer(serializers.ModelSerializer):
    """Вложенный сериализатор для вывода списка стран."""

    class Meta:
        fields = ("name",)
        model = Country


class GenreSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор для вывода списка жанров."""

    class Meta:
        fields = ("name",)
        model = Genre


class MovieListSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода списка фильмов."""

    class Meta:
        fields = ("id", "name", "release_year", "poster", "rating")
        model = Movie


class PersonSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор для вывода списка персон."""

    class Meta:
        fields = ("first_name", "last_name")
        model = Person


class PersonListSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода списка персон."""

    class Meta:
        fields = ("id", "first_name", "last_name", "picture", "birthdate")
        model = Person


class PersonDetailSerializer(serializers.ModelSerializer):
    """Подробное описание персоны."""

    country = serializers.SlugRelatedField(slug_field="name", read_only=True)
    my_votes = serializers.SerializerMethodField(
        read_only=True, method_name="get_votes")
    all_votes = serializers.ReadOnlyField(source="get_like_rating")
    all_likes = serializers.ReadOnlyField(source="get_like_count")
    all_dislikes = serializers.ReadOnlyField(source="get_dislike_count")
    age = serializers.ReadOnlyField(source="get_age")
    gender = serializers.ReadOnlyField(source="get_gender_display")

    class Meta:
        fields = (
            "first_name", "last_name", "birthdate", "age", "gender",
            "country", "picture", "description", "my_votes", "all_votes",
            "all_likes", "all_dislikes"
        )
        model = Person

    def get_votes(self, obj):
        request = self.context.get("request")
        content_type = ContentType.objects.get_for_model(obj)
        try:
            like = LikeDislike.objects.get(user=request.user, object_id=obj.id, content_type=content_type)
        except LikeDislike.DoesNotExist:
            return False
        return like.get_vote_display()


class MovieDetailSerializer(serializers.ModelSerializer):
    """Подробное описание фильма."""

    genres = GenreSerializer(read_only=True, many=True)
    countries = CountrySerializer(read_only=True, many=True)
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    actors = PersonSerializer(read_only=True, many=True)
    directors = PersonSerializer(read_only=True, many=True)
    is_in_bookmarks = serializers.SerializerMethodField(
        method_name="get_is_in_bookmarks", read_only=True)
    my_rating = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        fields = (
            "name", "release_year", "poster", "rating", "my_rating",
            "description", "category", "genres", "countries", "actors",
            "directors", "is_in_bookmarks", "comments"
        )
        model = Movie

    def get_is_in_bookmarks(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return obj.bookmarks.filter(user=request.user).exists()

    def get_my_rating(self, obj):
        request = self.context.get("request")
        ip = get_ip(request)
        try:
            rating = Rating.objects.get(movie_id=obj.id, ip=ip)
        except Rating.DoesNotExist:
            return False
        return rating.get_score_display()
