from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/farmer/', views.register_farmer, name='register_farmer'),
    path('register/buyer/', views.register_buyer, name='register_buyer'),
]