"""
URL configuration for Construction_assistant project.

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
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login/',views.login),
    # path('ad',views.admin),

    # register
    path('userRegister',views.userRegister),
    path('ConRegister',views.ConRegister),
    path('workerRegister',views.WorkerRegister),
    

    #Admin
    path('adminHome',views.adminHome),
    path('adminView_user',views.adminView_user),
    path('adminConView',views.adminConView),
    path('adminWorker',views.adminWorker),
    path('adminViewRequest',views.adminViewRequest),
    path('deleteUser',views.deleteUser),
    path('deleteWorkers',views.deleteWorkers),
    path('ApproveCon',views.ApproveCon),
    path('dltCon',views.dltCon),


    #User
    path('userHome',views.userHome),
    path('viewUserprofile',views.viewUserprofile),
    path('request_form',views.request_form),
    path('viewWorkers',views.viewWorkers),
    path('user_payment/',views.user_payment),
    path('userReq',views.userReq),
    path('useraddfeedback',views.useraddfeedback),
    path('updateUser',views.updateUser),
    path('viewUserfeedback',views.viewUserfeedback),
    path('view_assigned_workers',views.view_assigned_workers),
    path('request_worker_change',views.request_worker_change),
    path('user_view_con',views.user_view_con),



    #Contractor
    path('consHome',views.consHome),
    path('viewConsprofile',views.viewConsprofile),
    path('viewRequest',views.viewRequest),
    path('viewWorker',views.viewWorker),
    path('ApproveWorker',views.ApproveWorker),
    path('deleteWorker',views.deleteWorker),
    path('AssignWorker',views.AssignWorker),
    path('payWorker/',views.payWorker,name='payWorker'),
    path('user_paid',views.user_paid),
    path('deleteRequest',views.deleteRequest),
    path('updateContractor',views.updateContractor),
    path('contractor_feedback_view',views.contractor_feedback_view),
    path('assign_new_worker',views.assign_new_worker),
    path('view_worker_change_requests',views.view_worker_change_requests),

    #Worker
    path('workerHome/',views.workerHome),
    path('viewWorkerprofile/',views.viewWorkerprofile),
    path('updateWorker/',views.updateWorker),
    path('ViewWork/',views.ViewWork),
    path('ViewPayment/',views.ViewPayment),
    path('viewFeedback/',views.viewFeedback),
    path('workeraddfeedback/',views.workeraddfeedback),
    path('dl/',views.dlt),


    #-----Chat--------
    path('chat/',views.chat),
    path('reply/',views.reply),

    path('upload_work_images', views.upload_work_images),
    path('view_work_images', views.view_work_images),
    path('worker-details/<int:id>/', views.worker_details, name='worker_details'),
    path('contractor-details/<int:id>/', views.contractor_details, name='contractor_details'),
    path('user_add_contractor_feedback', views.user_add_contractor_feedback, name='user_add_contractor_feedback'),
    path('adm',views.adm),
      path('handle_worker_change/', views.handle_worker_change, name='handle_worker_change'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)