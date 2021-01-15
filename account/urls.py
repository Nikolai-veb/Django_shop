from django.urls import path
from . import views

urlpatterns = [
    path('login_cast', views.CustomLoginView.as_view(), name="login_cast"),
    path('register/', views.RegisterCustomUserView.as_view(), name='register'),
    path('custom_users/<int:pk>/', views.CustomerUserDetailView.as_view(), name='custom_users'),
    path('edit/<int:pk>/', views.EditCustomerUserView.as_view(), name='edit'),

]
