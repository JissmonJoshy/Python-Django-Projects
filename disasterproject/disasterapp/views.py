from asyncio.windows_events import NULL
import email
import re
from cv2 import add
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
import datetime
from django.core.files.storage import FileSystemStorage

from tomlkit import key
from .models import *

# import tkinter as tk
# from tkinter import messagebox

from django.contrib import messages


# Create your views here.


def udp(request):
    # alogin = Login.objects.create(
    #     uname='admin@gmail.com', password='admin', userType='admin')
    # authreg=CampMember.objects.filter(id=1).update(campid=1)
    # dupdate=DonationCommon.objects.filter(id=1).update(cardno='4916024821232688',cvv='765',mm='5',yy='2023')
    # authreg=Login.objects.get(uname='haritha@gmail.com').delete
    # allotfund=Claims.objects.filter(id=1).update(status='Pending')
    return HttpResponse("Successfull")


def index(request):
    return render(request, "index.html")


def logout(request):
    return render(request, "index.html")


def userhome(request):
    msg = request.GET.get("msg")
    ddata = Messages.objects.all()
    return render(request, "user/userhome.html", {"ddata": ddata, "msg": msg})


def workerhome(request):
    return render(request, "social worker/workerhome.html")


def adminhome(request):
    msg = request.GET.get("msg")
    return render(request, "admin/adminhome.html", {"msg": msg})


def authorityhome(request):
    return render(request, "authority/authorityhome.html")


def officerhome(request):
    msg = request.GET.get("msg")
    return render(request, "camp officer/officerhome.html", {"msg": msg})


def userviewprofile(request):
    uid = request.session["uid"]
    user = UserReg.objects.filter(id=uid)
    return render(request, "user/viewprofile.html", {"user": user})


def base(request):
    return render(request, "common/commonbase.html")


def login(request):
    msg = ""
    type = ""
    if request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        data = Login.objects.filter(uname=email, password=password)
        if data:
            data = Login.objects.get(uname=email, password=password)
            type = data.userType
            if data.userType == "admin":
                messages.success(request, "Login successful. Welcome back!")
            elif data.userType == "Social Worker":
                workerdata = SocialRegister.objects.get(email=email)
                uid = workerdata.id
                request.session["uid"] = uid
                messages.success(request, "Login successful. Welcome back!")
            elif data.userType == "User":
                userdata = UserReg.objects.get(email=email)
                uid = userdata.id
                request.session["uid"] = uid
                messages.success(request, "Login successful. Welcome back!")
            elif data.userType == "authority":
                authdata = AuthReg.objects.get(email=email)
                uid = authdata.id
                dist = authdata.district
                request.session["dist"] = dist
                request.session["uid"] = uid
                messages.success(request, "Login successful. Welcome back!")
            elif data.userType == "Camp Officer":
                authdata = OfficerReg.objects.get(email=email)
                uid = authdata.id
                request.session["uid"] = uid
                messages.success(request, "Login successful. Welcome back!")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "common/login.html", {"msg": msg, "type": type})


def userregister(request):
    msg = ""
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        state = request.POST.get("state")
        district = request.POST.get("district")
        address = request.POST.get("address")
        if UserReg.objects.filter(email=email).exists():
            msg = "Email Already Registered"
        else:
            abc = Login.objects.create(uname=email, password=password, userType="User")
            abc.save()
            reg = UserReg.objects.create(
                name=name,
                email=email,
                phone=phone,
                state=state,
                district=district,
                address=address,
                loginid=abc,
            )
            reg.save()
            msg = "Registration Successful"
        # return HttpResponseRedirect("/login")
    return render(request, "common/user_register.html", {"msg": msg})


def workerreg(request):
    msg = ""
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        state = request.POST.get("state")
        district = request.POST.get("district")
        address = request.POST.get("address")
        if SocialRegister.objects.filter(email=email).exists():
            msg = "Email Already Registered"
        else:
            abc = Login.objects.create(
                uname=email, password=password, userType="Social Worker"
            )
            abc.save()

            reg = SocialRegister.objects.create(
                name=name,
                email=email,
                phone=phone,
                state=state,
                district=district,
                address=address,
                loginid=abc,
            )
            reg.save()

            msg = "Registration Successful"
    return render(request, "common/worker_registration.html", {"msg": msg})


def officerreg(request):
    msg = ""
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        state = request.POST.get("state")
        district = request.POST.get("district")
        address = request.POST.get("address")

        if OfficerReg.objects.filter(email=email).exists():
            msg = "Email Already Registered"
        else:
            abc = Login.objects.create(
                uname=email, password=password, userType="Camp Officer"
            )
            abc.save()

            reg = OfficerReg.objects.create(
                name=name,
                email=email,
                phone=phone,
                state=state,
                district=district,
                address=address,
                loginid=abc,
            )
            reg.save()

            msg = "Registration Successful"
    return render(request, "common/officer_register.html", {"msg": msg})


###################### COMMON ######################
def userdonatemoney(request):
    msg = ""
    uid = request.session["uid"]
    filldata = UserReg.objects.filter(id=uid)
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        cardno = request.POST.get("cardno")
        cvv = request.POST.get("cvv")
        month = request.POST.get("month")
        year = request.POST.get("year")
        amount = request.POST.get("amount")

        dreguser = DonationRegUsers.objects.create(
            name=name,
            email=email,
            phone=phone,
            cardno=cardno,
            cvv=cvv,
            mm=month,
            yy=year,
            amount=amount,
            uid=uid,
        )
        dreguser.save()

        msg = "Successfully Donated"
    return render(
        request, "common/donatemoney.html", {"filldata": filldata, "msg": msg}
    )


def commondonatemoney(request):
    msg = ""
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        cardno = request.POST.get("cardno")
        cvv = request.POST.get("cvv")
        month = request.POST.get("month")
        year = request.POST.get("year")
        amount = request.POST.get("amount")

        dcommon = DonationCommon.objects.create(
            name=name,
            email=email,
            phone=phone,
            cardno=cardno,
            cvv=cvv,
            mm=month,
            yy=year,
            amount=amount,
        )
        dcommon.save()
        msg = "Donated Successfully"
        return HttpResponseRedirect("/index")
    return render(request, "common/commondonate.html", {"msg": msg})


###################### ADMIN ######################


def addauthority(request):
    msg = ""
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        state = request.POST.get("state")
        district = request.POST.get("district")
        if AuthReg.objects.filter(email=email).exists():
            msg = "Email Already Registered"
        else:
            abc = Login.objects.create(
                uname=email, password=password, userType="authority"
            )
            abc.save()

            addauth = AuthReg.objects.create(
                name=name,
                email=email,
                phone=phone,
                state=state,
                district=district,
                loginid=abc,
            )
            addauth.save()
            msg = "Authority Added Successfully"
        # return HttpResponseRedirect("/viewauth")
    return render(request, "admin/addauthority.html", {"msg": msg})


def adminviewauthority(request):
    vauth = AuthReg.objects.all()
    print(vauth)
    msg = request.GET.get("msg")
    return render(request, "admin/viewauthority.html", {"vauth": vauth, "msg": msg})


def deleteauthority(request):
    msg = ""
    if request.GET:
        id = request.GET.get("id")
        data = AuthReg.objects.filter(id=id).delete()
        msg = "Deleted Successfully"
    return HttpResponseRedirect("/viewauth?msg=" + msg)


def adminviewuserpayments(request):
    vpayment = DonationRegUsers.objects.all()
    return render(request, "admin/adminviewpayments.html", {"vpayment": vpayment})


def adminviewcommonpayments(request):
    vpayment = DonationCommon.objects.all()
    return render(request, "admin/adminviewcommonpayments.html", {"vpayment": vpayment})


def sendmessage(request):
    msg = ""
    if request.POST:
        message = request.POST.get("message")
        date = datetime.datetime.now()

        adminmsg = Messages.objects.create(subject=message, date=date)
        adminmsg.save()
        msg = "Message Sent Successfully"
        return HttpResponseRedirect("/adminhome?msg=" + msg)
    return render(request, "admin/sendmessage.html")


def viewclaimrequests(request):
    msg = request.GET.get("msg")
    crequest = Claims.objects.filter(status="Pending")
    allotted = Claims.objects.filter(status="Allotted")
    return render(
        request,
        "admin/viewclaimrequests.html",
        {"crequest": crequest, "allotted": allotted, "msg": msg},
    )


def allotfund(request):
    msg = ""
    cid = request.GET.get("id")
    cdata = Claims.objects.filter(id=cid)
    if request.POST:
        amount = request.POST.get("amount")
        allotfund = Claims.objects.filter(id=cid).update(
            samount=amount, status="Allotted"
        )
        msg = "Fund Allotted"
        return HttpResponseRedirect("/viewclaimrequests?msg=" + msg)
    return render(request, "admin/allotfund.html", {"cdata": cdata})


def adminviewcomplaints(request):
    abc = Complaint.objects.all()
    return render(request, "admin/viewcomplaints.html", {"abc": abc})


def replycomplaint(request):
    compid = request.GET.get("compid")
    if request.POST:
        reply = request.POST.get("reply")
        comp = Complaint.objects.filter(id=compid).update(reply=reply)
        print(comp)
        return HttpResponseRedirect("/admincomplaints")
    return render(request, "admin/replycomplaint.html")


def adminviewreports(request):
    rdata = Disaster.objects.all()
    return render(request, "admin/viewreports.html", {"rdata": rdata})


def verifyreport(request):
    if request.GET:
        id = request.GET.get("id")
        verify = Disaster.objects.filter(id=id).update(status="Verified")
        return HttpResponseRedirect("/adminviewreports")
    return render(request, "admin/viewreports.html")


def viewcamps(request):
    # campdata = CampReg.objects.filter(officerid=uid)
    campdata = CampReg.objects.filter(status="pending")
    approvedcamp = CampReg.objects.filter(status="approved")
    return render(
        request,
        "admin/viewcamps.html",
        {"campdata": campdata, "approvedcamp": approvedcamp},
    )


def approvecamp(request):
    cid = request.GET.get("id")
    action = CampReg.objects.filter(id=cid).update(status="approved")
    return HttpResponseRedirect("/viewcamps")


def rejectcamp(request):
    cid = request.GET.get("id")
    action = CampReg.objects.filter(id=cid).update(status="rejected")
    return HttpResponseRedirect("/viewcamps")


###################### USER ######################


def edtprofile(request):
    uid = request.session["uid"]
    edtprof = UserReg.objects.filter(id=uid)
    if request.POST:
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        state = request.POST.get("state")
        district = request.POST.get("district")
        address = request.POST.get("address")

        updatedata = UserReg.objects.filter(id=uid).update(
            name=name, phone=phone, state=state, district=district, address=address
        )
        # print(updatedata)

        logdata = Login.objects.filter(id=uid).update(password=password)
        return HttpResponseRedirect("/usrprofile")
    return render(request, "user/editprofile.html", {"edtprof": edtprof})


def applyclaim(request):
    msg = ""
    msg = request.GET.get("msg")
    uid = request.session["uid"]
    cdata = Claims.objects.filter(uid=uid)
    if request.POST:
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        state = request.POST.get("state")
        district = request.POST.get("district")
        damages = request.POST.get("damages")
        bankname = request.POST.get("bankname")
        aadhaar = request.POST.get("aadhaar")
        accno = request.POST.get("accno")
        ifsc = request.POST.get("ifsc")
        branch = request.POST.get("branch")
        address = request.POST.get("address")
        image = request.FILES["imgfile"]

        claim = Claims.objects.create(
            uid=uid,
            fname=fname,
            lname=lname,
            email=email,
            phone=phone,
            state=state,
            district=district,
            damages=damages,
            bankname=bankname,
            aadhaar=aadhaar,
            accno=accno,
            ifsc=ifsc,
            branch=branch,
            address=address,
            image=image,
            status="Pending",
        )
        claim.save()
        msg = "Applied Successfully"
        return HttpResponseRedirect("/applyclaim?msg=" + msg)
    return render(request, "user/applyclaim.html", {"cdata": cdata, "msg": msg})


def reportdisaster(request):
    msg = ""
    msg = request.GET.get("msg")
    uid = request.session["uid"]
    ddata = Disaster.objects.filter(uid=uid)
    if request.POST:
        disaster = request.POST.get("category")
        location = request.POST.get("location")
        state = request.POST.get("state")
        district = request.POST.get("district")
        date = datetime.datetime.now()
        img = request.FILES["txtfile"]
        des = request.POST.get("description")

        rdisaster = Disaster.objects.create(
            uid=uid,
            disaster=disaster,
            location=location,
            state=state,
            district=district,
            date=date,
            des=des,
            image=img,
        )
        rdisaster.save()
        msg = "Disaster reported successfully"
        return HttpResponseRedirect("/reportdisaster?msg=" + msg)
    return render(request, "user/reportdisaster.html", {"ddata": ddata, "msg": msg})


def complaint(request):
    msg = ""
    uid = request.session["uid"]
    abc = UserReg.objects.get(id=uid)
    compp = Complaint.objects.filter(uid_id=uid)
    if request.POST:
        issue = request.POST.get("issue")
        description = request.POST.get("description")
        date = datetime.datetime.now()

        comp = Complaint.objects.create(
            uid=abc, issue=issue, description=description, date=date
        )
        comp.save()
        msg = "Complaint Raised"
        return HttpResponseRedirect("/userhome?msg=" + msg)
    return render(request, "user/makecomplaint.html", {"compp": compp, "msg": msg})


def userviewrequirements(request):
    msg = request.GET.get("msg")
    zero = 0
    uvreq = CampRequirements.objects.filter(status="Requested")
    return render(
        request,
        "user/userviewrequirements.html",
        {"uvreq": uvreq, "zero": zero, "msg": msg},
    )


def userviewnotification(request):
    ndata = Messages.objects.all().order_by("date").reverse()[:5]
    return render(request, "user/userviewnotification.html", {"ndata": ndata})


def searchpeople(request):
    result = ""
    msg = ""
    if request.POST:
        keyword = request.POST.get("search")
        result = CampMember.objects.filter(name__contains=keyword)
        print(result)

        # return HttpResponseRedirect("#contact")
        if result == []:
            msg = "No Matching Result"
    return render(request, "user/searchpage.html", {"result": result, "msg": msg})


def donaterequirements(request):
    cid = request.GET.get("cid")
    rid = request.GET.get("rid")
    uid = request.session["uid"]
    zero = 0
    abc = CampRequirements.objects.filter(id=rid)
    req = abc[0].quantity
    name = abc[0].name
    print(req)
    if request.POST:
        itemname = request.POST.get("itemname")
        quantity = request.POST.get("quantity")

        fqty = int(req) - int(quantity)
        donate = UserDonation.objects.create(
            uid=uid, campid=cid, itemname=itemname, quantity=quantity
        )
        donate.save()
        update = CampRequirements.objects.filter(id=rid).update(quantity=fqty)
        print(update)
        msg = "You Will be Contacted Soon"
        return HttpResponseRedirect("/userhome?msg=" + msg)
    return render(
        request,
        "user/donaterequirements.html",
        {"name": name, "zero": zero, "req": req},
    )


###################### AUTHORITY ######################


def viewmessages(request):
    vmsg = Messages.objects.all()
    return render(request, "authority/authorityviewmessages.html", {"vmsg": vmsg})


def viewdisasters(request):
    dist = request.session["dist"]
    vdis = Disaster.objects.filter(status="Verified").filter(district=dist)
    return render(request, "authority/authorityviewdisaster.html", {"vdis": vdis})


def takeaction(request):
    id = request.GET.get("id")
    if request.POST:
        reply = request.POST.get("reply")
        abc = Messages.objects.filter(id=id).update(status="Viewed", reply=reply)
        return HttpResponseRedirect("/viewmsg")
    return render(request, "authority/reporttoadmin.html")


def viewteam(request):
    dist = request.session["dist"]
    uid = request.session["uid"]

    data = RescueTeam.objects.filter(district=dist)
    print(list(data))
    print(dist)

    # team=RescueTeam.objects.filter()

    return render(request, "authority/viewteam.html", {"data": data})


def action(request):
    id = request.GET.get("id")
    update = Disaster.objects.filter(id=id).update(status="Responded")
    return render(request, "authority/authorityviewdisaster.html")


def viewauthProfile(request):
    uid = request.session["uid"]
    data = AuthReg.objects.filter(id=uid)
    return render(request, "authority/authprofile.html", {"data": data})


def autheditprof(request):
    msg = ""
    id = request.GET.get("id")
    data = AuthReg.objects.filter(loginid=id)
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        state = request.POST.get("state")
        district = request.POST.get("district")

        update = AuthReg.objects.filter(loginid=id).update(
            name=name, email=email, phone=phone, state=state, district=district
        )
        uplogin = Login.objects.filter(id=id).update(uname=email, password=password)
        msg = "Profile Updated"
        return HttpResponseRedirect("/authprofile?msg=" + msg)
    return render(request, "authority/autheditprofile.html", {"data": data})


###################### Social Worker ######################


def viewdisaster(request):
    vdisaster = Disaster.objects.all()
    return render(request, "social worker/viewdisaster.html", {"vdisaster": vdisaster})


def jointeam(request):
    uid = request.session["uid"]
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        date = request.POST.get("date")
        state = request.POST.get("state")
        district = request.POST.get("district")
        address = request.POST.get("address")

        join = RescueTeam.objects.create(
            uid=uid,
            name=name,
            email=email,
            phone=phone,
            date=date,
            state=state,
            district=district,
            address=address,
        )
        join.save()
        return HttpResponseRedirect("/workerhome")
    return render(request, "social worker/rescueteam.html")


def viewworkerprofile(request):
    uid = request.session["uid"]
    data = SocialRegister.objects.filter()
    return render(request, "social worker/workerprofile.html", {"data": data})


def workereditprofile(request):
    id = request.GET.get("id")
    data = SocialRegister.objects.filter(loginid=id)
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        state = request.POST.get("state")
        district = request.POST.get("district")
        address = request.POST.get("address")

        update = SocialRegister.objects.filter(loginid=id).update(
            name=name,
            email=email,
            phone=phone,
            state=state,
            district=district,
            address=address,
        )
        logupdate = Login.objects.filter(id=id).update(uname=email, password=password)
        return HttpResponseRedirect("/workerprofile")
    return render(request, "social worker/workereditprofile.html", {"data": data})


###################### Camp Officer ######################


def registercamp(request):
    msg = ""
    uid = request.session["uid"]
    odata = OfficerReg.objects.filter(id=uid)
    if request.POST:
        name = request.POST.get("campername")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        date = datetime.datetime.now()
        members = request.POST.get("members")
        state = request.POST.get("state")
        district = request.POST.get("district")
        address = request.POST.get("address")

        if CampReg.objects.filter(email=email).exists():
            msg = "Camp Already Added"

        else:
            regcamp = CampReg.objects.create(
                officerid=uid,
                name=name,
                email=email,
                phone=phone,
                date=date,
                members=members,
                state=state,
                district=district,
                address=address,
                status="pending",
            )
            regcamp.save()
            return HttpResponseRedirect("/officerviewcamps")
    return render(
        request, "camp officer/registercamp.html", {"odata": odata, "msg": msg}
    )


def deletecamp(request):
    id = request.GET.get("id")
    cdelete = CampReg.objects.filter(id=id).delete()
    return HttpResponseRedirect("/regcamp")


def officerviewcamps(request):
    uid = request.session["uid"]
    campdata = CampReg.objects.filter(officerid=uid).filter(status="pending")
    approvedcamp = CampReg.objects.filter(officerid=uid).filter(status="approved")
    return render(
        request,
        "camp officer/viewcamps.html",
        {"campdata": campdata, "approvedcamp": approvedcamp},
    )


def addmember(request):
    msg = ""
    cdata = ""
    uid = request.session["uid"]
    if CampReg.objects.filter(officerid=uid).filter(status="approved").exists():
        abc = CampReg.objects.get(officerid=uid)
        cmpid = abc.id
        cdata = CampMember.objects.filter(campid=cmpid)
        if request.POST:
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            age = request.POST.get("age")
            state = request.POST.get("state")
            district = request.POST.get("district")
            address = request.POST.get("address")

            addmember = CampMember.objects.create(
                campid=abc,
                name=name,
                email=email,
                phone=phone,
                age=age,
                state=state,
                district=district,
                address=address,
            )
            addmember.save()
            return HttpResponseRedirect("/addmember")
    else:
        msg = "No Registered Camps"
        return HttpResponseRedirect("/officerhome?msg=" + msg)
    return render(request, "camp officer/addmember.html", {"cdata": cdata, "msg": msg})


def deletemember(request):
    id = request.GET.get("id")
    mdelete = CampMember.objects.filter(id=id).delete()
    return HttpResponseRedirect("/addmember")


def addrequirements(request):
    msg = ""
    uid = request.session["uid"]

    if CampReg.objects.filter(officerid=uid).filter(status="approved").exists():
        abc = CampReg.objects.get(officerid=uid, status="approved")
        if request.POST:
            name = request.POST.get("itemname")
            quantity = request.POST.get("quantity")
            date = datetime.datetime.now()
            remarks = request.POST.get("remarks")

            addreq = CampRequirements.objects.create(
                campid=abc,
                officerid=uid,
                name=name,
                quantity=quantity,
                date=date,
                remarks=remarks,
            )
            addreq.save()

            return HttpResponseRedirect("/viewreq")
    else:
        msg = "No Registered Camps"
        return HttpResponseRedirect("/officerhome?msg=" + msg)
    return render(request, "camp officer/requirements.html")


def officerviewrequirements(request):
    msg = ""
    creq = NULL
    uid = request.session["uid"]
    if CampRequirements.objects.filter(officerid=uid):
        creq = CampRequirements.objects.filter(officerid=uid)
    else:
        msg = "Register A Camp First"
        return HttpResponseRedirect("/officerhome?msg=" + msg)
    return render(request, "camp officer/officerviewrequirements.html", {"creq": creq})


def officerviewnotification(request):
    ndata = Messages.objects.all().order_by("date").reverse()[:5]
    return render(
        request, "camp officer/officerviewnotification.html", {"ndata": ndata}
    )


def officerprofile(request):
    uid = request.session["uid"]
    data = OfficerReg.objects.filter(id=uid)
    return render(request, "camp officer/officerprofile.html", {"data": data})


def officereditprofile(request):
    id = request.GET.get("id")
    odata = OfficerReg.objects.filter(loginid=id)
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        state = request.POST.get("state")
        district = request.POST.get("district")
        address = request.POST.get("address")

        udata = OfficerReg.objects.filter(loginid=id).update(
            name=name,
            email=email,
            phone=phone,
            state=state,
            district=district,
            address=address,
        )

        logdata = Login.objects.filter(id=id).update(uname=email, password=password)

        return HttpResponseRedirect("/officerprofile")
    return render(request, "camp officer/officereditprofile.html", {"odata": odata})
