from django.shortcuts import render
from .models import Actor
from .forms import ActorForm
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy


def index(request):
    return render(request, "movies/index.html")


class ActorView(ListView):
    model = Actor
    template_name = "movies/actor_list.html"
    extra_context = {"title": "Актеры"}


class ActorCreateView(CreateView):
    form_class = ActorForm
    template_name = "movies/actor_create.html"
    success_url = reverse_lazy("movies:actors")
    extra_context = {"title": "Создание нового актера"}
