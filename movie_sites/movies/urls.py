from django.urls import path
from .views import index, ActorView, ActorCreateView


app_name = "movies"

urlpatterns = [
    path("", index, name="index"),
    path("actors/", ActorView.as_view(), name="actors"),
    path("actors/create/", ActorCreateView.as_view(), name="actor_create"),
]
