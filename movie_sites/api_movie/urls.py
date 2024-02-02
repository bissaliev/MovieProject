from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MovieViewSet, PersonViewSet

app_name = "api"

router = DefaultRouter()

router.register("movies", MovieViewSet, basename="movies")
router.register("persons", PersonViewSet, basename="persons")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt"))
]
