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
    path('buyer/dashboard/add-product-need/', views.add_product_need, name='add_product_need'),
    path('buyer/dashboard/product-need/<int:need_id>/edit/', views.edit_product_need, name='edit_product_need'),
    path('buyer/dashboard/product-need/<int:need_id>/delete/', views.delete_product_need, name='delete_product_need'),
    path('buyer/dashboard/product-need/<int:need_id>/update-status/', views.update_product_need_status, name='update_product_need_status'),
    path('buyer/dashboard/add-certification/', views.add_company_certification, name='add_company_certification'),
    path('buyer/dashboard/certification/<int:certification_id>/edit/', views.edit_company_certification, name='edit_company_certification'),
    path('buyer/dashboard/certification/<int:certification_id>/delete/', views.delete_company_certification, name='delete_company_certification'),
    path('buyer/home/', views.buyer_home_page, name='buyer_home'),
    path('buyer/<int:buyer_id>/profile/', views.view_buyer_profile, name='view_buyer_profile'),
    path('farmer/<int:farmer_id>/profile/', views.view_farmer_profile, name='view_farmer_profile'),
    path('farmer/<int:farmer_id>/review/', views.leave_farmer_review, name='leave_farmer_review'),
    path('buyer/<int:buyer_id>/review/', views.leave_buyer_review, name='leave_buyer_review'),
    path('farmer/community/create/', views.create_community, name='create_community'),
    path('farmer/community/<int:community_id>/', views.community_detail, name='community_detail'),
    path('farmer/community/<int:community_id>/join/', views.join_community, name='join_community'),
    path('farmer/community/<int:community_id>/leave/', views.leave_community, name='leave_community'),
    path('farmer/communities/browse/', views.browse_communities, name='browse_communities'),
    path('farmer/community/<int:community_id>/edit/', views.edit_community, name='edit_community'),
    path('guides/market-preparation/', views.market_preparation_guides, name='market_preparation_guides'),
    path('guides/certification-help/', views.certification_help, name='certification_help'),
    path('register/logistic/', views.register_logistic, name='register_logistic'),
    path('login/logistic/', views.logistic_login, name='logistic_login'),
    path('logistic/dashboard/', views.logistic_dashboard, name='logistic_dashboard'),
    path('logistic/dashboard/update-logo/', views.update_logistic_logo, name='update_logistic_logo'),
    path('logistic/dashboard/edit-profile/', views.edit_logistic_profile, name='edit_logistic_profile'),
    path('logistic/<int:logistic_id>/profile/', views.view_logistic_profile, name='view_logistic_profile'),
    path('farmer/order-history/', views.order_history, name='order_history'),
    path('buyer/order-history/', views.buyer_order_history, name='buyer_order_history'),
    path('tutorials/videos/', views.video_tutorials, name='video_tutorials'),
    #path('buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    #path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
]