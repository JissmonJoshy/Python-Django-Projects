"""
URL configuration for crime_shield_project project.

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
from crime_shield_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dlt/',views.dlt),
    # path('adm',views.adm),

    path('',views.index,name='index'),
    path('logins',views.logins,name='logins'),
    path('view_login',views.view_login,name='view_login'),
    # path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('police_department_dashboard',views.police_department_dashboard,name='police_department_dashboard'),
    path('police_department_register',views.police_department_register,name='police_department_register'),
    path('user_register/', views.user_register, name='user_register'),
    path('add_law/', views.add_law, name='add_law'),
    path('view_laws/', views.view_laws, name='view_laws'),
    path('user_view_laws/', views.user_view_laws, name='user_view_laws'),
    path('user_register_complaint/', views.user_register_complaint, name='user_register_complaint'),
    path('user_view_complaints/', views.user_view_complaints, name='user_view_complaints'),

    path('police_view_complaints/', views.police_view_complaints, name='police_view_complaints'),
    path('update_complaint_status/<int:complaint_id>/', views.update_complaint_status, name='update_complaint_status'),

    path('add_case_report/<int:complaint_id>/', views.add_case_report, name='add_case_report'),
    path('view_case_report/<int:complaint_id>/', views.view_case_report, name='view_case_report'),

    path('user_case_reports/', views.user_case_reports, name='user_case_reports'),

    path('report_missing_person/', views.report_missing_person, name='report_missing_person'),
    path('my_missing_cases/', views.my_missing_cases, name='my_missing_cases'),
    path('police_missing_cases/', views.police_missing_cases, name='police_missing_cases'),
    path('update_missing_status/<int:missing_id>/', views.update_missing_status, name='update_missing_status'),
    path('add_report_missing/<int:missing_id>/', views.add_report_missing, name='add_report_missing'),
    path('view_missing_report/<int:case_id>/', views.view_missing_report, name='view_missing_report'),

    path('user_view_missing_reports/', views.user_view_missing_reports, name='user_view_missing_reports'),


    path('report_crime/', views.report_crime, name='report_crime'),
    path('my_crime_reports/', views.my_crime_reports, name='my_crime_reports'),
    path('police_crime_reports/', views.police_crime_reports, name='police_crime_reports'),
    path('update_crime_status/<int:report_id>/', views.update_crime_status, name='update_crime_status'),
    path('add_case_report_crime/<int:crime_id>/', views.add_case_report_crime, name='add_case_report_crime'),
    path('view_crime_report/<int:case_id>/', views.view_crime_report, name='view_crime_report'),
    path('user_view_crime_reports/', views.user_view_crime_reports, name='user_view_crime_reports'),


    path('search_missing_person/', views.search_missing_person, name='search_missing_person'),
    path('view_missing_report_search/<int:case_id>/', views.view_missing_report_search, name='view_missing_report_search'),

    path('search_complaints/', views.search_complaints, name='search_complaints'),
    path('view_complaint_report_search/<int:complaint_id>/', views.view_complaint_report_search, name='view_complaint_report_search'),

    path('search_crimereports/', views.search_crimereports, name='search_crimereports'),
    path('view_crime_report_search/<int:crime_id>/', views.view_crime_report_search, name='view_crime_report_search'),



    path('view_all_reports/', views.view_all_reports, name='view_all_reports'),## not used here ##
    path('police_profile/', views.police_profile, name='police_profile'),
    path('user_profile/', views.user_profile, name='user_profile'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)