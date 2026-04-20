"""
URL configuration for attendance_project project.

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
from django.contrib import admin
from django.urls import path
from attendance_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('dlt/', views.dlt, name='dlt'),
    # path('ad/', views.admin, name='admin'),
    path('logins/', views.logins, name='logins'),
    path('student_register/', views.student_register, name='student_register'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('teacher_register/', views.teacher_register, name='teacher_register'),

    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    

    path('display_students/', views.display_students, name='display_students'),
    path('display_teachers/', views.display_teachers, name='display_teachers'),
    path('approve_teacher/<int:teacher_id>/', views.approve_teacher, name='approve_teacher'),
    path('reject_teacher/<int:teacher_id>/', views.reject_teacher, name='reject_teacher'),

    path('student_profile/', views.student_profile, name='student_profile'),
    path('teacher_profile/', views.teacher_profile, name='teacher_profile'),

    path('assign_teacher/', views.assign_teacher, name='assign_teacher'),
    path("display_assigned_teachers/", views.display_assigned_teachers, name="display_assigned_teachers"),
    path("mark_attendance/", views.mark_attendance, name="mark_attendance"),
    path("manage_attendance/", views.manage_attendance, name="manage_attendance"),
    path("attendance_percentage/", views.attendance_percentage, name="attendance_percentage"),
    path("student_attendance/", views.student_attendance, name="student_attendance"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

