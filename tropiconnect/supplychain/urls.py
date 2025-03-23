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
    path('farmer/dashboard/edit-profile/', views.edit_farmer_profile, name='edit_farmer_profile'),
    path('farmer/dashboard/farm/<int:farm_id>/add-photo/', views.add_farm_photo, name='add_farm_photo'),
    path('farmer/dashboard/photo/<int:photo_id>/delete/', views.delete_farm_photo, name='delete_farm_photo'),
    path('farmer/dashboard/add-farm/', views.add_farm, name='add_farm'),
    path('farmer/dashboard/add-product/', views.add_product, name='add_product'),
    path('farmer/dashboard/product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('farmer/dashboard/product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('farmer/home/', views.farmer_home_page, name='farmer_home'),
    path('farmer/dashboard/add-certification/', views.farmer_add_certification, name='farmer_add_certification'),
    path('farmer/dashboard/certification/<int:certification_id>/edit/', views.farmer_edit_certification, name='farmer_edit_certification'),
    path('farmer/dashboard/certification/<int:certification_id>/delete/', views.farmer_delete_certification, name='farmer_delete_certification'),
    path('buyer/dashboard/edit-profile/', views.edit_buyer_profile, name='edit_buyer_profile'),
    #path('buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    #path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
]