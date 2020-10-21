from django.shortcuts import render
from .models import Article, Comment
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

class ArticleListView(ListView):
    """Обработчик статей"""
    model = Article
    context_object_name = "articles"
    queryset = Article.objects.filter(draft=False)


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

