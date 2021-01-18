from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentForm, ShareArticleForm
from .models import Article, Comment, Tag
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import View
from .service import send

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


class FormShareEmailView(DetailView):
    """Form Share Email"""
    model = Article
    context_object_name = "article"
    pk_url_kwarg = 'pk'
    template_name = "blog/share.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ShareArticleForm()
        return context


class ShareEmailView(View):
    """Handler and Send Email"""
    def post(self, request, slug):
        form = ShareArticleForm(request.POST)
        article = get_object_or_404(Article, slug=slug)
        if form.is_valid():
            cd = form.cleaned_data
            comment = cd['comments']
            user_name = cd['name']
            head = f'{article.title}'
            body = f'{article.image} \n {article.body} \n This massage to {user_name}, \n {comment}'
            user_email = cd['email']
            send(head,body,user_email)
        else:
            form = ShareArticleForm()
        return redirect("article_list")