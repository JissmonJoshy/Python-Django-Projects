"""
URL configuration for BeautyParlour project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from myapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dlt',views.dlt,name='dlt'),
    path('',views.index),
    path('register_expert/',views.register_expert),
    path('register_customer/',views.register_customer),
    path('login/',views.login),
    
    # ADMIN
    path('adminHome/',views.adminHome),
    path('viewCustomers/',views.viewCustomers),
    path('deleteCustomer/',views.deleteCustomer),
    path('adminViewServices/',views.adminViewServices),
    path('deleteService/',views.deleteService),
    path('addPackage/',views.addPackage),
    
    
    
    # Customer
    path('customerHome/',views.customerHome,name='customerHome'),
    
    path('viewExperts/',views.viewExperts),
    path('deleteExperts/',views.deleteExperts),

    path('add_skintone/', views.add_skintone, name='add_skintone'),

    
    path('payment_page/<int:service_id>/', views.payment_page, name='payment_page'),

    path('customer/booking-success/', views.booking_success, name="booking_success"),

    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('assign_expert/<int:booking_id>/', views.assign_expert, name='assign_expert'),
    path('schedule_service/<int:booking_id>/', views.schedule_service,name='schedule_service'),
    
    path('customer_bookings/', views.customer_bookings, name='customer_bookings'),
    path('view_skins/', views.view_skins),

    path('chat/',views.chat),
    path('reply/',views.reply),

    path('expertHome',views.expertHome,name='expertHome'),
    path('assigned_customers/', views.expert_assigned_customers, name='assigned_customers'),
    path('all_skins/', views.all_skins, name='all_skins'), 
    path('send_skin_message/<int:skin_id>/', views.send_skin_message, name='send_skin_message'),

     
    path('update_skin_tone/<int:skin_id>/', views.update_skin_tone, name='update_skin_tone'),
    path('send_skin_message/<int:skin_id>/', views.send_skin_message, name='send_skin_message'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)