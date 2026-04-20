"""
URL configuration for autoservice project.

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
from app1 import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('dlt',views.dlt),
    path('userhome/', views.userhome),
    path('servicehome/', views.servicehome),
    path('adminhome/', views.adminhome),
    path('login/', views.login),
    path('servicereg/', views.servicereg),
    path('customerreg/', views.customerreg),
    path('ad/', views.ad),
    path('billview/', views.billview),

    path('customer_list/', views.customer_list, name='customer_list'),
    path('approve_customer/', views.approve_customer, name='approve_customer'),
    path('reject_customer/', views.reject_customer, name='reject_customer'),

    


# Admin
    path('service_center/',views.service_center,name='service_center'),
    path('approve_center/',views.approve_center),
    path('reject_center/',views.reject_center),
    path('delete_center',views.delete_center,name='delete_center'),



# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^____________Servicer__________^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    path('customer_approve/', views.customer_approve),
    path('accept/', views.accept),
    path('reject/', views.reject),
    path('approveservice_request/', views.approveservice_request),
    path('customer_rquest/', views.customer_rquest),
    path('delivery_list/', views.delivery_list),
    path('acceptagent/', views.acceptagent),
    path('rejectagent/', views.rejectagent),
    path('completeser/', views.completeser),
    path('sparelist_ser/', views.sparelist_ser),
    path('addcart/', views.addcart),
    path('cartlist/', views.cartlist),
    path('deletecartid/', views.deletecartid),
    path('order/', views.order),
    path('payment/', views.payment),
    path('orderdetails/', views.orderdetails),
    path('chat/', views.chat),
    path('add_amount/', views.add_amount),

# ___________________________________________ CUSTOMER  __________________________________________

    path('service_centerview/', views.service_centerview,name='service_centerview'),
    path('servicerequest/', views.servicerequest,name='servicerequest'),
    path('requestdetails/', views.requestdetails,name='requestdetails'),
    path('delete_data/', views.delete_data),
    path('sell_vechile/', views.sell_vechile,name='sell_vechile'),
    path('vechile_list/', views.vechile_list),
    path('userfeedback/', views.userfeedback),
    path('vechile_buylist/', views.vechile_buylist),
    path('approve_vechile/', views.approve_vechile),
    path('vehicle_rejectq/', views.vehicle_rejectq),
    path('reply/', views.reply),




path('payment/', views.payment),
path('update_payment/', views.update_payment),
path("service/feedbacks/", views.service_feedbacks, name="service_feedbacks"),
path("admin_feedbacks/", views.admin_feedbacks, name="admin_feedbacks"),

path('give_feedback/<int:service_id>/',views.give_feedback,name='give_feedback'),
path('view_feedback/', views.view_feedback, name='view_feedback'),
path('delete_feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)