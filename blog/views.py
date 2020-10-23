from django.shortcuts import render, get_object_or_404
from .models import Article, Comment, Tag
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

class ArticleListView(ListView):
    """Обработчик статей"""
    model = Article
    context_object_name = "articles"

    def get_queryset(self, tag_slug=None):
        queryset = Article.objects.filter(draft=True)
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = Article.objects.filter(tags__in=[tag])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class ArticleDetailView(DetailView):
    "Оработчик статьи"
    model = Article
    id_field = "pk"



class AddComment(View):
    """Обработчик комментариев"""
    def post(self, request, pk):
        article = Article.objects.get(id=pk, draft=False)
        form = CommentForm(self.request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if self.request.POST.get("parent", None):
                form.parent_id = (self.request.POST.get("parent"))
            form.article = article
            form.save()
        return redirect(article.get_absolute_url())

