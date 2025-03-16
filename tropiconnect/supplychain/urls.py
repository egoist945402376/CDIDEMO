from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/farmer/', views.register_farmer, name='register_farmer'),
    path('register/buyer/', views.register_buyer, name='register_buyer'),
    path('login/farmer/', views.farmer_login, name='farmer_login'),
    path('login/buyer/', views.buyer_login, name='buyer_login'),
    path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('dashboard/update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('dashboard/update-company-logo/', views.update_company_logo, name='update_company_logo'),
    path('logout/', views.logout_view, name='logout'),
    #path('buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    #path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
]