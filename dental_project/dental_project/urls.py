"""
URL configuration for dental_project project.

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
from dental_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('view_login/',views.view_login,name='view_login'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('admin_dashboard',views.admin_dashboard, name='admin_dashboard'),
    path('lab_dashboard',views.lab_dashboard,name='lab_dashboard'),
    path('patient_dashboard',views.patient_dashboard,name='patient_dashboard'),
    path('dentist_dashboard',views.dentist_dashboard,name='dentist_dashboard'),
    # path('ad',views.admin),

    path('patient-register/', views.patient_register, name='patient_register'),
    path('dentist_register/', views.dentist_register, name='dentist_register'),
    path('lab_register/', views.lab_register, name='lab_register'),
    
    path('display_all_dentist',views.display_all_dentist,name='display_all_dentist'),
    path('display_all_patient',views.display_all_patient,name='display_all_patient'),
    path('display_all_lab',views.display_all_lab,name='display_all_lab'),

    path('patient_profile/', views.patient_profile, name='patient_profile'),
    path('dentist_profile/', views.dentist_profile, name='dentist_profile'),
    path('lab_profile/', views.lab_profile, name='lab_profile'),
    path('view_dentist_reviews/<int:dentist_id>/', views.view_dentist_reviews, name='view_dentist_reviews'),
    
    path('approve_patient/<int:patient_id>/', views.approve_patient, name='approve_patient'),
    path('reject_patient/<int:patient_id>/', views.reject_patient, name='reject_patient'),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),

    path('approve_dentist/<int:dentist_id>/', views.approve_dentist, name='approve_dentist'),
    path('reject_dentist/<int:dentist_id>/', views.reject_dentist, name='reject_dentist'),
    path('delete_dentist/<int:dentist_id>/', views.delete_dentist, name='delete_dentist'),

    path('approve_lab/<int:lab_id>/', views.approve_lab, name='approve_lab'),
    path('reject_lab/<int:lab_id>/', views.reject_lab, name='reject_lab'),
    path('delete_lab/<int:lab_id>/', views.delete_lab, name='delete_lab'),

    path('add-schedule/', views.add_schedule, name='add_schedule'),
    path('schedules',views.display_all_schedule,name='display_all_schedule'),

    path('edit-schedule/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),
    path('delete-schedule/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),

    path('dentist-schedules/', views.display_all_dentist_schedule, name='display_all_dentist_schedule'),
    path('book_appointments/<int:schedule_id>/', views.book_appointments, name='book_appointments'),
    path('dentist-appointments/', views.dentist_appointments, name='dentist_appointments'),
    path('update_appointment_status/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
    path('dentist-calendar/', views.dentist_calendar, name='dentist_calendar'),

    path('schedule-appointment/', views.schedule_appointment, name='schedule_appointment'),
    path('display_confirmed_patients/', views.display_confirmed_patients, name='display_confirmed_patients'),
    path('display_assigned_patients/', views.display_assigned_patients, name='display_assigned_patients'),
    path('delivery_orders', views.delivery_orders, name='delivery_orders'),
    path('mark_delivered/<int:order_id>/', views.mark_order_delivered, name='mark_order_delivered'),

    path('confirm_payment/<int:appointment_id>/', views.confirm_payment, name='confirm_payment'),
    path('my-bookings/',views.patient_bookings, name='patient_bookings'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),


    path('assigned-labs/', views.assigned_lab_view, name='assigned_lab_view'),
    path('make-payment/<int:lab_order_id>/', views.make_payment, name='make_payment'),

    path('request-order/', views.request_order, name='request_order'),
    path('manage-requests/', views.manage_requests, name='manage_requests'),
    path('update-request/<int:request_id>/<str:action>/', views.update_request_status, name='update_request_status'),
    path('lab/requests/', views.lab_requests_view, name='lab_requests_view'),

   
    path('leave_review/<int:appointment_id>/', views.leave_review, name='leave_review'),
    path('view_reviews', views.view_reviews, name='admin_reviews'),

    path('admin_lab_orders/', views.admin_lab_orders, name='admin_lab_orders'),

    path('patient_reviews/', views.patient_reviews, name='patient_reviews'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)