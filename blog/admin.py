from django.contrib import admin
from .models import Article, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ( "id", "user", "title", "slug", "draft")
    list_filter = ("title",)
    search_fields = ("title",)
   # prepopulated_fields = {"slug": ("title","user")}
    autocomplete_lookup_fields = {"slug":["title", "user"]}
    list_editable = ("draft",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_dislay = ("name", "email", "parent", "article")
    list_filter = ("name", "email", "article", "create")
    searche_fields = ("name", "article")
