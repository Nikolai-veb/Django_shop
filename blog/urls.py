from django.urls import path
from . import views


urlpatterns = [
    path("article/", views.ArticleListView.as_view(), name="article_list"),
    path("article/<slug:tag_slug>/", views.ArticleListView.as_view(), name="article_list_by_tag"),
    path("<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("comment/<int:pk>/", views.AddComment.as_view(), name="add_comment"),
]
