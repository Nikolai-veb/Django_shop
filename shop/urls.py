from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path("<int:id>/<slug:slug>/", views.product_detail, name='product_detail'),
    path("add-rating/", views.add_rating_star, name='add_rating'),
    path("review/<int:pk>/", views.add_review, name='add_review'),

]
