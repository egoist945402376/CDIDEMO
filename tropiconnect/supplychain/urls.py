from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/farmer/', views.register_farmer, name='register_farmer'),
    path('register/buyer/', views.register_buyer, name='register_buyer'),
    path('login/farmer/', views.farmer_login, name='farmer_login'),
    path('login/buyer/', views.buyer_login, name='buyer_login'),
    path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('dashboard/update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    #path('buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    #path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
]