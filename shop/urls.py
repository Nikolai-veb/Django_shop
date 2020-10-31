from django.urls import path
from . import views
#from django.contrib.auth.decorators import login_required

#from .models import BookmarkProduct, BookmarkReview


urlpatterns = [
    path("", views.ProductListView.as_view(), name='product_list'),
    path("filter/", views.FilterProduct.as_view(), name="filter"),
    path("search/", views.SearchProduct.as_view(), name="search"),
    path("sorte/", views.SorteProduct.as_view(), name="sorte"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path("add-rating/", views.add_rating_star, name='add_rating'),
    path("review/<int:pk>/", views.AddReview.as_view(), name='add_review'),
]
