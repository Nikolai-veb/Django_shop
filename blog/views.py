from django.shortcuts import render
from .models import Article
from django.views.generic import ListView, DetailView


class ArticleListView(ListView):
    """Обработчик статей"""
    model = Article
    context_object_name = "articles"
    queryset = Article.objects.filter(draft=False)


class ArticleDetailView(DetailView):
    "Оработчик статьи"
    model = Article
    id_field = "pk"
