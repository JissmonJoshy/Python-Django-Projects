"""
URL configuration for agrishop_prject project.

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
from agrishop_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('adm/',views.adm,name='adm'),
    path('dlt/',views.dlt,name='dlt'),

    path('',views.index,name='index'),
    path('logins/',views.logins,name='logins'),
    path('view_login/',views.view_login,name='view_login'),

    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
    path('farmer_dashboard/',views.farmer_dashboard,name='farmer_dashboard'),
    path('delivery_dashboard/',views.delivery_dashboard,name='delivery_dashboard'),

    path('user_register/',views.user_register, name='user_register'),
    path('farmer_register/',views.farmer_register, name='farmer_register'),
    path('delivery_register/',views.delivery_register, name='delivery_register'),

    path('view_registered_users/',views.view_registered_users, name='view_registered_users'),
    path('accept_user/<int:user_id>/',views.accept_user, name='accept_user'),
    path('reject_user/<int:user_id>/',views.reject_user, name='reject_user'),
    path('delete_user/<int:user_id>/',views.delete_user, name='delete_user'),
    

    path('view_registered_farmers/',views.view_registered_farmers, name='view_registered_farmers'),
    path('accept_farmer/<int:farmer_id>/',views.accept_farmer, name='accept_farmer'),
    path('reject_farmer/<int:farmer_id>/',views.reject_farmer, name='reject_farmer'),
    path('delete_farmer/<int:farmer_id>/',views.delete_farmer, name='delete_farmer'),

    path('view_registered_delivery/',views.view_registered_delivery, name='view_registered_delivery'),
    path('accept_delivery/<int:delivery_id>/',views.accept_delivery, name='accept_delivery'),
    path('reject_delivery/<int:delivery_id>/',views.reject_delivery, name='reject_delivery'),
    path('delete_delivery/<int:delivery_id>/',views.delete_delivery, name='delete_delivery'),

    path('view_profile_farmer/',views.view_profile_farmer, name='view_profile_farmer'),
    path('edit_profile_farmer/',views.edit_profile_farmer, name='edit_profile_farmer'),

    path('view_profile_delivery/',views.view_profile_delivery, name='view_profile_delivery'),
    path('edit_profile_delivery/',views.edit_profile_delivery, name='edit_profile_delivery'),

    path('view_profile_user/',views.view_profile_user, name='view_profile_user'),
    path('edit_profile_user/',views.edit_profile_user, name='edit_profile_user'),

    path('add_product/',views.add_product, name='add_product'),
    path('farmer_added_products/',views.farmer_added_products, name='farmer_added_products'),
    path('edit_product/<int:pid>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:pid>/', views.delete_product, name='delete_product'),

    path('admin_products/', views.admin_products, name='admin_products'),
    path('accept_product/<int:id>/', views.accept_product, name='accept_product'),
    path('reject_product/<int:id>/', views.reject_product, name='reject_product'),

    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_favorite/<int:product_id>/', views.add_to_favorite, name='add_to_favorite'),
    path('view_favorites/', views.view_favorites, name='view_favorites'),
    path('remove_favorite/<int:fav_id>/', views.remove_favorite, name='remove_favorite'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('increase_quantity/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove_cart_item/<int:cart_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('view_checkout/', views.view_checkout, name='view_checkout'),
    path('admin_view_all_checkouts/', views.admin_view_all_checkouts, name='admin_view_all_checkouts'),
    path('assign_delivery/<int:checkout_id>/', views.assign_delivery, name='assign_delivery'),
    path('display_all_products/', views.display_all_products, name='display_all_products'),

    path('delivery_assigned_orders/', views.delivery_assigned_orders, name='delivery_assigned_orders'),
    path('update_delivery_status/<int:checkout_id>/', views.update_delivery_status, name='update_delivery_status'),
    path('verify_payment_status/<int:checkout_id>/', views.verify_payment_status, name='verify_payment_status'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('view_reviews/', views.view_reviews, name='view_reviews'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),

    path('admin_product_analytics/', views.admin_product_analytics, name='admin_product_analytics'),
    path('add_supply/', views.add_supply, name='add_supply'),
    path('display_supply/', views.display_supply, name='display_supply'),

    path('farmer_orders/', views.farmer_orders, name='farmer_orders'),
    path('farmer_reviews/', views.farmer_reviews, name='farmer_reviews'),
    path('display_supply_farmer/', views.display_supply_farmer, name='display_supply_farmer'),
    path('add_to_cart_supply/<int:supply_id>/', views.add_to_cart_supply, name='add_to_cart_supply'),

    path('cart_supply/', views.cart_supply, name='cart_supply'),
    path('increase_supply/<int:order_id>/', views.increase_supply, name='increase_supply'),
    path('decrease_supply/<int:order_id>/', views.decrease_supply, name='decrease_supply'),
    path('remove_supply/<int:order_id>/', views.remove_supply, name='remove_supply'),
    path('checkout_supply/', views.checkout_supply, name='checkout_supply'),
    path('view_my_supply_orders.html', views.view_my_supply_orders, name='view_my_supply_orders'),

    path('all_supply_orders_admin/', views.all_supply_orders_admin, name='all_supply_orders_admin'),
    path('assign_delivery_supply/<int:order_id>/', views.assign_delivery_supply, name='assign_delivery_supply'),
    path('delivery_assigned_supply_orders/',views.delivery_assigned_supply_orders,name='delivery_assigned_supply_orders'),
    path('update_supply_delivery_status/<int:checkout_id>/', views.update_supply_delivery_status, name='update_supply_delivery_status'),
    path('verify_supply_payment_status/<int:checkout_id>/', views.verify_supply_payment_status, name='verify_supply_payment_status'),
    path('submit_supply_review/<int:checkout_id>/', views.submit_supply_review, name='submit_supply_review'),
    path('view_my_supply_reviews/', views.view_my_supply_reviews, name='view_my_supply_reviews'),
    path('view_all_my_reviews/', views.view_all_my_reviews, name='view_all_my_reviews'),
    path('delete_supply_review/<int:review_id>/', views.delete_supply_review, name='delete_supply_review'),

    path('add_to_favorite_supply/<int:supply_id>/', views.add_to_favorite_supply, name='add_to_favorite_supply'),
    path('view_favorites_supply/', views.view_favorites_supply, name='view_favorites_supply'),
    path('remove_favorite_supply/<int:fav_id>/', views.remove_favorite_supply, name='remove_favorite_supply'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)