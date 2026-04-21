"""disasterproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from disasterapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('udp/', views.udp),
    path('index/', views.index),
    path('', views.index),
    path('logout/', views.logout),
    path('base/', views.base),
    path('login/', views.login),
    path('usrreg/', views.userregister),
    path('workerhome/', views.workerhome),
    path('userhome/', views.userhome),
    path('adminhome/', views.adminhome),
    path('authorityhome/', views.authorityhome),
    path('officerhome/', views.officerhome),
    path('workerreg/', views.workerreg),
    path('officerreg/', views.officerreg),
    path('addauth/', views.addauthority),
    path('viewauth/', views.adminviewauthority),
    path('usrprofile/', views.userviewprofile),
    path('edtprof/', views.edtprofile),
    path('donatemoney/', views.userdonatemoney),
    path('commondonatemoney/', views.commondonatemoney),
    path('adminviewuserpayments/', views.adminviewuserpayments),
    path('adminviewcommonpayments/', views.adminviewcommonpayments),
    path('viewclaimrequests/', views.viewclaimrequests),
    path('allotfund/', views.allotfund),
    path('sendmessage/', views.sendmessage),
    path('viewmsg/', views.viewmessages),
    path('reply/', views.takeaction),
    path('applyclaim/', views.applyclaim),
    path('reportdisaster/', views.reportdisaster),
    path('viewdisaster/', views.viewdisaster),
    path('regcamp/', views.registercamp),
    path('deletecamp/', views.deletecamp),
    path('addmember/', views.addmember),
    path('deletemember/', views.deletemember),
    path('addrequirements/', views.addrequirements),
    path('complaints/', views.complaint),
    path('usrviewrequirements/', views.userviewrequirements),
    path('notifications/', views.userviewnotification),
    path('search/', views.searchpeople),
    path('donaterequirements/', views.donaterequirements),
    path('admincomplaints/', views.adminviewcomplaints),
    path('compreply/', views.replycomplaint),
    path('jointeam/', views.jointeam),
    path('viewteam/', views.viewteam),
    path('adminviewreports/', views.adminviewreports),
    path('verifyreport/', views.verifyreport),
    path('viewdisasters/', views.viewdisasters),
    path('action/', views.action),
    path('viewcamps/', views.viewcamps),
    path('approvecamp/', views.approvecamp),
    path('officerviewcamps/', views.officerviewcamps),
    path('rejectcamp/', views.rejectcamp),
    path('viewreq/', views.officerviewrequirements),
    path('officerviewnotification/', views.officerviewnotification),
    path('authprofile', views.viewauthProfile),
    path('authedtprof/', views.autheditprof),
    path('workerprofile/', views.viewworkerprofile),
    path('workereditprofile/', views.workereditprofile),
    path('officerprofile/', views.officerprofile),
    path('officereditprof/', views.officereditprofile),
    path('deleteauthority/', views.deleteauthority),
]
