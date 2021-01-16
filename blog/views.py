from django.shortcuts import  get_object_or_404, redirect
from .forms import CommentForm
from .models import Article, Comment, Tag
from django.views.generic import ListView, DetailView
from django.views.generic.base import View


class ArticleListView(ListView):
    """Articles List"""
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "articles"

    def get_queryset(self, tag_slug=None):
        queryset = Article.objects.filter(draft=False)
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = Article.objects.filter(tags__in=[tag])
        return queryset



class ArticleDetailView(DetailView):
    """Article Detail"""
    context_object_name = "article"
    model = Article
    id_field = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['recommended'] = Article.objects.filter(tags__in=context['article'].tags.all())
        return context


class AddComment(View):
    """Comments"""

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

