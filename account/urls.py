from django.urls import path
from . import views

urlpatterns = [
    path('login_cast', views.CastomLoginView.as_view(), name="login_cast"),
    path('register/', views.register, name='register'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),

]
