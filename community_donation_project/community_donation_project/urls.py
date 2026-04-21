"""
URL configuration for community_donation_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from community_donation_app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('view_login',views.view_login,name='view_login'),

    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('donor_dashboard',views.donor_dashboard,name='donor_dashboard'),
    path('ngo_dashboard',views.ngo_dashboard,name='ngo_dashboard'),

    path('donor_register',views.donor_register,name='donor_register'),
    path('ngo_register',views.ngo_register,name='ngo_register'),

    path('display_all_ngo',views.display_all_ngo,name='display_all_ngo'),
    path('display_all_donor',views.display_all_donor,name='display_all_donor'),
    path('view_donation_transactions', views.view_donation_transactions, name='view_donation_transactions'),

    path('approve_donor/<int:donor_id>/', views.approve_donor, name='approve_donor'),
    path('reject_donor/<int:donor_id>/', views.reject_donor, name='reject_donor'),
    path('delete_donor/<int:donor_id>/', views.delete_donor, name='delete_donor'),


    path('approve_ngo/<int:ngo_id>/', views.approve_ngo, name='approve_ngo'),
    path('reject_ngo/<int:ngo_id>/', views.reject_ngo, name='reject_ngo'),
    path('delete_ngo/<int:ngo_id>/', views.delete_ngo, name='delete_ngo'),

    path('view_profile_ngo/', views.view_profile_ngo, name='view_profile_ngo'),
    path('ngo-profile/edit/', views.edit_profile_ngo, name='edit_profile_ngo'),

    path('add_donation/', views.add_donation, name='add_donation'),
    path('view-donations/', views.view_donations, name='view_donations'),
    path('edit-donation/<int:donation_id>/', views.edit_donation, name='edit_donation'),
    path('delete-donation/<int:donation_id>/', views.delete_donation, name='delete_donation'),

    path('view_profile_donor',views.view_profile_donor,name='view_profile_donor'),
    path('edit_profile/', views.edit_profile_donor, name='edit_profile_donor'),
    path('display_all_donations',views.display_all_donations,name='display_all_donations'),
    path('donate/<int:donation_id>/', views.make_donation, name='make_donation'),

    path('admin_view_donations',views.admin_view_donations,name='admin_view_donations'),
    path('ngo_donations_received/', views.ngo_donations_received, name='ngo_donations_received'),

    path('my_donations/',views.my_donations,name='my_donations'),

    path('chat/', views.chat, name='chat'),
    path('reply/', views.reply, name='reply'),
    path('generate_report',views.generate_report,name='generate_report'),
    path('deactivate_donation/<int:donation_id>/', views.deactivate_donation, name='deactivate_donation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
