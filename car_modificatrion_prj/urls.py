"""
URL configuration for car_modificatrion_prj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from car_modificatrion_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('adm',views.adm,name='adm'),
    path('user_register/', views.user_register, name='user_register'),
    path('employee_register/', views.employee_register, name='employee_register'),
    path('login/', views.login_view, name='login'),

   

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),

    path('view_users/', views.view_users, name='view_users'),
    path('view_employees/', views.view_employees, name='view_employees'),
    path('approve_employee/<int:login_id>/', views.approve_employee, name='approve_employee'),
    path('reject_employee/<int:login_id>/', views.reject_employee, name='reject_employee'),

    # User profile
    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_profile_edit/', views.user_profile_edit, name='user_profile_edit'),

    # Employee profile
    path('employee_profile/', views.employee_profile, name='employee_profile'),
    path('employee_profile_edit/', views.employee_profile_edit, name='employee_profile_edit'),
    path('add_services/', views.add_services, name='add_services'),
    path('view_services/', views.view_services, name='view_services'),
    path('edit_services/<int:service_id>/', views.edit_services, name='edit_services'),
    path('delete_services/<int:service_id>/', views.delete_services, name='delete_services'),

    path('user_view_services/', views.user_view_services, name='user_view_services'),
    path('book_service/<int:service_id>/', views.book_service, name='book_service'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('delete_service_booking/<int:id>/', views.delete_service_booking, name='delete_service_booking'),


    path('all_bookings/', views.all_bookings, name='all_bookings'),
    path('update_booking_status/<int:booking_id>/<str:status>/',views.update_booking_status,name='update_booking_status'),
    path('assign-booking/<int:booking_id>/',views.assign_booking,name='assign_booking'),
    path('make_payment/<int:booking_id>/', views.make_payment, name='make_payment'),
    path('assigned_works/', views.assigned_works, name='assigned_works'),
    path('add_parts/', views.add_parts, name='add_parts'),
    path('view_parts/', views.view_parts, name='view_parts'),
    path('edit_part/<int:part_id>/', views.edit_part, name='edit_part'),
    path('delete_part/<int:part_id>/', views.delete_part, name='delete_part'),

    path('user_view_parts/', views.user_view_parts, name='user_view_parts'),
    path('book_part/<int:part_id>/', views.book_part, name='book_part'),
    path('my_part_bookings/', views.my_part_bookings, name='my_part_bookings'),
    
    path('delete_part_booking/<int:booking_id>/', views.delete_part_booking, name='delete_part_booking'),
    path('part_payment/<int:id>/', views.part_payment, name='part_payment'),

    path('all_parts_bookings/', views.all_parts_bookings, name='all_parts_bookings'),
    path("mark_part_delivered/<int:id>/",views.mark_part_delivered,name="mark_part_delivered"),

    path('update_work_progress/<int:id>/', views.update_work_progress, name='update_work_progress'),

    path('employee_parts/', views.view_employee_parts, name='view_employee_parts'),
    path('book_employee_part/<int:part_id>/', views.book_employee_part, name='book_employee_part'),
    path('employee_part_bookings/', views.employee_part_bookings, name='employee_part_bookings'),
    path('employee_payment/<int:booking_id>/', views.employee_payment, name='employee_payment'),

    path('admin_view_employee_part_bookings/', views.admin_view_employee_part_bookings, name='admin_view_employee_part_bookings'),
    path('admin_mark_employee_part_delivered/<int:booking_id>/', views.admin_mark_employee_part_delivered, name='admin_mark_employee_part_delivered'),



        
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
