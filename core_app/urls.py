# core_app/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='core_app/auth/login.html',
        next_page='dashboard'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Home and Dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.member_dashboard, name='dashboard'),
    
    # Resources
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('resources/create/', views.resource_create, name='resource_create'),
    
    # Bookings
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/create/<int:resource_id>/', views.booking_create, name='booking_create'),
    path('bookings/<int:pk>/approve/', views.booking_approve, name='booking_approve'),
    
    # Subscriptions
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('subscriptions/create/', views.subscription_create, name='subscription_create'),
    
    # Leases
    path('leases/', views.lease_list, name='lease_list'),
    path('leases/create/<int:resource_id>/', views.lease_create, name='lease_create'),
    
    # User Management (Staff/Admin only)
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
]