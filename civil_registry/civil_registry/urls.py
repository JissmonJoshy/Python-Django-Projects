"""
URL configuration for civil_registry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from civilapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('index',views.index),
    path('services',views.services,name='services'),
    path('addregistrar/',views.addregistrar,name='addregistrar'),
    path('login/',views.login,name='login'),
    path('registration/',views.registration,name='registration'),
    path('addauthority/',views.addauthority,name='addauthority'),
    path('viewauthority/',views.viewauthority,name='viewauthority'),
    path('updateauth/',views.updateauth,name='updateauth'),
    path('deleteauth/',views.deleteauth,name='deleteauth'),

    # homes
    path('userhome/',views.userhome,name='userhome'),
    path('rtohome/',views.rtohome,name='rtohome'),
    path('rpohome/',views.rpohome,name='rpohome'),
    path('echome/',views.echome,name='echome'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('registrarhome/',views.registrarhome,name='registrarhome'),
    path('guest/',views.guest,name='guest'),
    path('help/',views.help,name='help'),

    path('addfeedback/',views.addfeedback,name='addfeedback'),
    path('viewfeedback/',views.viewfeedback,name='viewfeedback'),



# birth
    path('applybirth/',views.applybirth,name='applybirth'),
    path('adminapplybirth/',views.adminapplybirth,name='adminapplybirth'),
    path('deletebirth/',views.deletebirth,name='deletebirth'),
    path('forwardbirth/',views.forwardbirth,name='forwardbirth'),
    path('regbirth/',views.regbirth,name='regbirth'),
    path('assignbirth/',views.assignbirth,name='assignbirth'),

    path('deletebirthreg/',views.deletebirthreg,name='deletebirthreg'),
    path('withdrawbirth/',views.withdrawbirth,name='withdrawbirth'),
    path('statusbirth/',views.statusbirth,name='statusbirth'),
    path('paymentbirth/',views.paymentbirth,name='paymentbirth'),

# death
    path('applydeath/',views.applydeath,name='applydeath'),
    path('adminapplydeath/',views.adminapplydeath,name='adminapplydeath'),
    path('deletedeath/',views.deletedeath,name='deletedeath'),
    path('forwarddeath/',views.forwarddeath,name='deletedeath'),
    path('regdeath/',views.regdeath,name='regdeath'),
    path('deletedeathreg/',views.deletedeathreg,name='deletedeathreg'),
    path('withdrawdeath/',views.withdrawdeath,name='withdrawdeath'),
    path('statusdeath/',views.statusdeath,name='statusdeath'),
    path('paymentdeath/',views.paymentdeath,name='paymentdeath'),
    path('assigndeath/',views.assigndeath,name='assigndeath'),
#  marriage
    path('applymarriage/',views.applymarriage,name='applymarriage'),
    path('adminapplymarriage/',views.adminapplymarriage,name='adminapplymarriage'),
    path('deletemarriage/',views.deletemarriage,name='deletemarriage'),
    path('forwardmarriage/',views.forwardmarriage,name='forwardmarriage'),
    path('regmarriage/',views.regmarriage,name='regmarriage'),
    path('deletemarriagereg/',views.deletemarriagereg,name='deletemarriagereg'),
    path('withdrawmarriage/',views.withdrawmarriage,name='withdrawmarriage'),
    path('statusmarriage/',views.statusmarriage,name='statusmarriage'),
    path('paymentmarriage/',views.paymentmarriage,name='paymentmarriage'),
    path('assignmarriage/',views.assignmarriage,name='assignmarriage'),
# license
    path('applylicense/',views.applylicense,name='applylicense'),
    path('adminapplylicense/',views.adminapplylicense,name='adminapplylicense'),
    path('deletelicense/',views.deletelicense,name='deletelicense'),
    path('forwardlicense/',views.forwardlicense,name='forwardlicense'),
    path('rtolicense/',views.rtolicense,name='rtolicense'),
    path('deletelicenserto/',views.deletelicenserto,name='deletelicenserto'),
    path('withdrawlicense/',views.withdrawlicense,name='withdrawlicense'),
    path('statuslicense/',views.statuslicense,name='statuslicense'),
    path('paymentlicense/',views.paymentlicense,name='paymentlicense'),

    # passport   
     path('applypassport/',views.applypassport,name='applypassport'),
    path('adminapplypassport/',views.adminapplypassport,name='adminapplypassport'),
    path('deletepassport/',views.deletepassport,name='deletepassport'),
    path('forwardpassport/',views.forwardpassport,name='forwardpassport'),
    path('rpopassport/',views.rpopassport,name='rpopassport'),
    path('deletepassportrpo/',views.deletepassportrpo,name='deletepassportrpo'),
    path('withdrawpassport/',views.withdrawpassport,name='withdrawpassport'),
    path('statuspassport/',views.statuspassport,name='statuspassport'),
    path('paymentpassport/',views.paymentpassport,name='paymentpassport'),

    # voters
    path('applyvoters/',views.applyvoters,name='applyvoters'),
    path('adminapplyvoters/',views.adminapplyvoters,name='adminapplyvoters'),
    path('deletevoters/',views.deletevoters,name='deletevoters'),
    path('forwardvoters/',views.forwardvoters,name='forwardvoters'),
    path('ecvoters/',views.ecvoters,name='ecvoters'),
    path('deletevotersec/',views.deletevotersec,name='deletevotersec'),
    path('withdrawvoters/',views.withdrawvoters,name='withdrawvoters'),
    path('statusvoters/',views.statusvoters,name='statusvoters'),
    path('paymentvoters/',views.paymentvoters,name='paymentvoters'),

    path('approvevoters/', views.approvevoters, name='approvevoters'),



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)