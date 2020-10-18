from django.urls import path
from . import views
#from django.contrib.auth.decorators import login_required

#from .models import BookmarkProduct, BookmarkReview


urlpatterns = [
   # path("", views.product_list, name='product_list'),
    path("", views.ProductListView.as_view(), name='product_list'),
    path("sorte/", views.sorte_product, name="sorte"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path("sorte/", views.sorte_product, name="sorte"),
    path("add-rating/", views.add_rating_star, name='add_rating'),
    path("review/<int:pk>/", views.add_review, name='add_review'),
]
