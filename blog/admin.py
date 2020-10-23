from django.contrib import admin
from .models import Article, Comment, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ( "name", "slug")
    list_filter = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ( "id", "user", "title", "slug", "draft")
    list_filter = ("title", "tags")
    search_fields = ("title", "tags")
    prepopulated_fields = {"slug": ("title","user")}
    list_editable = ("draft",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_dislay = ("name", "email", "parent", "article")
    list_filter = ("name", "email", "article", "create")
    searche_fields = ("name", "article")
