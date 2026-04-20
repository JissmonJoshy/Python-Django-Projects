from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import *
import os
from django.conf import settings
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO


# Create your views here.

####################### home #############################

def index(request):
    return render(request, 'index.html')


def guest(request):
    return render(request, 'guest.html')


def services(request):
    return render(request, 'services.html')


def login(request):

    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        print(username, "######################", password)
        # Retrieve the user object
        user = authenticate(username=username, password=password)
        print(user)

        if user is not None:
            if user.usertype == 'admin':
                request.session['uid'] = user.id
                request.session['type'] = 'admin'
                print("Admin login success")
                messages.info(request, "Admin login success")
                return redirect('/adminhome')
            elif user.usertype == 'rto':
                request.session['uid'] = user.id
                request.session['type'] = 'rto'
                print("rto login success")
                messages.info(request, "rto login success")
                return redirect('/rtohome')
            elif user.usertype == 'rpo':
                request.session['uid'] = user.id
                request.session['type'] = 'rpo'
                print("rpo login success")
                messages.info(request, "rpo login success")
                return redirect('/rpohome')
            elif user.usertype == 'registrar':
                request.session['uid'] = user.id
                request.session['type'] = 'registrar'
                print("registrar login success")
                messages.info(request, "registrar login success")
                return redirect('/registrarhome')
            elif user.usertype == 'election':
                request.session['uid'] = user.id
                request.session['type'] = 'election'
                print("registrar login success")
                messages.info(request, "ec login success")
                return redirect('/echome')

            elif user.usertype == 'user':
                request.session['uid'] = user.id
                request.session['type'] = 'user'
                print("registrar login success")
                messages.info(request, "user login success")
                return redirect('/userhome')
        else:
            print("Login Failed")
            messages.info(request, " login Failed")

    return render(request, 'login.html')


def adminhome(request):
    return render(request, 'admin/adminhome.html')


def userhome(request):
    return render(request, 'user/userhome.html')


def rtohome(request):
    return render(request, 'rto/rtohome.html')


def registrarhome(request):
    return render(request, 'registrar/registrarhome.html')


def rpohome(request):
    return render(request, 'rpo/rpohome.html')


def echome(request):
    return render(request, 'ec/echome.html')


def registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone')
        district = request.POST.get('district')
        aadhar = request.POST.get('aadhar')
        address = request.POST.get('address')
        if Login.objects.filter(username=email).exists():
            print("User already exists")
            messages.info(request, "already exists")
        else:
            loginqry = Login.objects.create_user(
                username=email, password=password, viewpassword=password, usertype='user')
            loginqry.save()

            ex = Registration.objects.create(
                name=name,
                email=email,
                password=password,
                phone_number=phone_number,
                district=district,
                aadhar=aadhar,
                user=loginqry,
                address=address,

            )
            ex.save()
            messages.info(request, "Registered successfully")

            return redirect('/login')

    return render(request, 'registration.html')


##################### admin ######################
def addauthority(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone')
        district = request.POST.get('district')
        authority = request.POST.get('authority')
        if Login.objects.filter(username=email).exists():
            print("Authority already exists")
            messages.info(request, "email already exists")

        if Addauthority.objects.filter(district=district, authority=authority).exists():
            print("authority already exist")
            messages.info(request, "registrar already exists")

        else:
            loginqry = Login.objects.create_user(
                username=email, password=password, viewpassword=password, usertype=authority)
            loginqry.save()

            ex = Addauthority.objects.create(
                name=name,
                email=email,
                password=password,
                phone_number=phone_number,
                district=district,
                authority=authority,
                user=loginqry,


            )
            ex.save()
            messages.info(request, "Authority Registered successfully")

            return redirect('/viewauthority')

    return render(request, 'admin/addauthority.html')


def addregistrar(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        taluk = request.POST.get('taluk')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone')
        district = request.POST.get('district')
        if Login.objects.filter(username=email).exists():
            print("Email  already exists")
            messages.info(request, "Email already in use")

        else:
            loginqry = Login.objects.create_user(
                username=email, password=password, viewpassword=password, usertype='registrar')
            loginqry.save()
        if Addauthority.objects.filter(taluk=taluk, district=district, authority='registrar').exists():
            print("Registrar already exist")
            messages.info(request, "registrar already exists")

        else:
            ex = Addauthority.objects.create(
                name=name,
                email=email,
                taluk=taluk,
                password=password,
                phone_number=phone_number,
                district=district,
                authority='registrar',
                user=loginqry,


            )
            ex.save()
            messages.info(request, "Authority Registered successfully")

            return redirect('/viewauthority')

    return render(request, 'admin/addregistrar.html')


def viewauthority(request):
    res = Addauthority.objects.all()
    return render(request, 'admin/viewauthority.html', {"res": res})


def deleteauth(request):
    id = request.GET.get('id')

    Login.objects.filter(id=id).delete()
    messages.info(request, "deleted")

    return HttpResponseRedirect('/viewauthority')


def updateauth(request):
    id = request.GET.get('id')

    res = Addauthority.objects.filter(id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        district = request.POST.get('district')
        authority = request.POST.get('authority')
        registerqry = Addauthority.objects.get(id=id)
        registerqry.name = name
        registerqry.email = email
        registerqry.phone_number = phone_number
        registerqry.district = district
        registerqry.authority = authority

        registerqry.save()
        messages.info(request, "updated")

        return redirect('/viewauthority')

    return render(request, 'admin/updateauth.html', {"res": res})

# birth starts here$$$$$$$$$$$$$$$$$$$$$$$


def applybirth(request):
    uid = request.session['uid']
    uuid = Registration.objects.get(user_id=uid)
    if request.method == 'POST':
        # Process the form data
        name = request.POST['name']
        father = request.POST['father']
        mother = request.POST['mother']

        gender = request.POST['gender']
        dob = request.POST['dob']
        birthplace = request.POST['birthplace']
        birth = request.POST['birth']
        relation = request.POST['relation']
        taluk = request.POST.get('taluk')

        district = request.POST['district']
        address = request.POST['address']
        identification = request.POST['identification']
        idproof = request.FILES['idproof']
        if Birth.objects.filter(name=name, dob=dob,).exists():
            messages.info(request, "already exists")
        else:
            # Create a new User instance and save it
            user = Birth(
                name=name,
                father=father,
                mother=mother,
                gender=gender,
                relation=relation,
                dob=dob,
                birthplace=birthplace,
                birth=birth,
                taluk=taluk,
                district=district,
                address=address,
                identification=identification,
                idproof=idproof,
                user=uuid
            )
        user.save()
        messages.info(request, " applied for birth certificate ")
        # Redirect to a success page or do something else
        return redirect('/paymentbirth')
    return render(request, 'user/applybirth.html')


def adminapplybirth(request):
    res = Birth.objects.filter(status='pending', payment_status='success')
    return render(request, 'admin/adminapplybirth.html', {"res": res})


def deletebirth(request):
    id = request.GET.get('id')
    Birth.objects.filter(id=id).delete()
    messages.info(request, " deleted")
    return HttpResponseRedirect('/adminapplybirth')


def deletebirthreg(request):
    id = request.GET.get('id')
    Birth.objects.filter(id=id).delete()
    messages.info(request, " deleted ")

    return HttpResponseRedirect('/regbirth')


def forwardbirth(request):
    id = request.GET.get('id')
    bb = Birth.objects.get(id=id)
    res = Addauthority.objects.filter(
        district=bb.district, authority='registrar')
    messages.info(request, " Forwarded ")

    return render(request, 'admin/forwardbirth.html', {'res': res, 'bb': bb})


def assignbirth(request):
    rid = request.GET.get('rid')
    bid = request.GET.get('bid')
    bb = Birth.objects.get(id=bid)
    reg = Addauthority.objects.get(id=rid)
    bb.status = 'forwarded'
    bb.save()
    Assign.objects.create(birth=bb, registrar=reg)
    messages.info(request, " Forwarded ")

    return redirect('/adminapplybirth')


def regbirth(request):
    uid = request.session['uid']
    uuid = Addauthority.objects.get(user_id=uid)
    res = Assign.objects.filter(
        birth__payment_status='success', birth__status='forwarded', registrar=uuid.id)
    if request.POST:
        certificate = request.FILES.get('certificate')
        print(certificate)
        bid = request.POST['bid']
        reb = Assign.objects.get(id=bid)
        reb.status = 'approved'
        reb.save()
        rel = Birth.objects.get(id=reb.birth_id)
        rel.certificate = certificate
        rel.status = 'approved'
        rel.save()
        messages.info(request, " Approved")

    return render(request, 'registrar/regbirth.html', {"res": res})


def statusbirth(request):
    uid = request.session['uid']
    print(uid)
    result = Birth.objects.filter(user_id__user_id=uid, status='approved')
    res = Birth.objects.filter(user_id__user_id=uid, status='pending')
    resul = Birth.objects.filter(user_id__user_id=uid, status='forwarded')
    return render(request, 'user/statusbirth.html', {"res": res, "resul": resul, "result": result})


def withdrawbirth(request):
    id = request.GET.get('id')
    Birth.objects.filter(id=id).delete()
    messages.info(request, " withdrawed ")
    return HttpResponseRedirect('/statusbirth')


def paymentbirth(request):
    id = request.GET.get('id')
    uid = request.session['uid']
    if request.POST:
        Birth.objects.filter(user_id__user_id=uid, status='pending').update(
            payment_status='success')
        messages.info(request, "Suceess")
        return redirect('/statusbirth')
    return render(request, 'user/payment.html')

# death starts here$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


def applydeath(request):
    uid = request.session['uid']
    uuid = Registration.objects.get(user_id=uid)
    if request.method == 'POST':
        # Process the form data
        name = request.POST['name']
        father = request.POST['father']
        mother = request.POST['mother']

        gender = request.POST['gender']
        dob = request.POST['dob']
        dod = request.POST['dod']
        taluk = request.POST.get('taluk')

        deathplace = request.POST['deathplace']
        death = request.POST['death']
        relation = request.POST['relation']

        district = request.POST['district']
        address = request.POST['address']
        identification = request.POST['identification']
        idproof = request.FILES['idproof']
        type = request.POST['type']
        if Death.objects.filter(name=name, dob=dob, dod=dod).exists():
            print("already applied ")
            messages.info(request, "already exists")
        else:

            # Create a new User instance and save it
            user = Death(
                name=name,
                father=father,
                mother=mother,
                gender=gender,
                relation=relation,
                dob=dob,
                dod=dod,
                deathplace=deathplace,
                death=death,
                taluk=taluk,
                district=district,
                address=address,
                identification=identification,
                idproof=idproof,
                type=type,
                user=uuid
            )
        user.save()
        messages.info(request, " applied for death certificate ")
        # Redirect to a success page or do something else
        return redirect('/paymentdeath')
    return render(request, 'user/applydeath.html')


def adminapplydeath(request):
    res = Death.objects.filter(status='pending', payment_status='success')
    return render(request, 'admin/adminapplydeath.html', {"res": res})


def deletedeath(request):
    id = request.GET.get('id')
    Death.objects.filter(id=id).delete()
    messages.info(request, " deleted ")

    return HttpResponseRedirect('/adminapplydeath')


def forwarddeath(request):
    id = request.GET.get('id')
    bb = Death.objects.get(id=id)
    res = Addauthority.objects.filter(
        district=bb.district, authority='registrar')

    return render(request, 'admin/forwarddeath.html', {'res': res, 'bb': bb})


def assigndeath(request):
    rid = request.GET.get('rid')
    bid = request.GET.get('bid')
    bb = Death.objects.get(id=bid)
    reg = Addauthority.objects.get(id=rid)
    bb.status = 'forwarded'
    bb.save()
    Assign.objects.create(death=bb, registrar=reg)
    messages.info(request, " assign")

    return redirect('/adminapplydeath')


def deletedeathreg(request):
    id = request.GET.get('id')
    Death.objects.filter(id=id).delete()
    messages.info(request, " deleteed ")

    return HttpResponseRedirect('/regdeath')


def regdeath(request):
    uid = request.session['uid']
    uuid = Addauthority.objects.get(user_id=uid)
    res = Assign.objects.filter(
        death__payment_status='success', death__status='forwarded', registrar=uuid.id)
    if request.POST:
        certificate = request.FILES.get('certificate')
        print(certificate)
        bid = request.POST['bid']
        reb = Assign.objects.get(id=bid)
        reb.status = 'approved'
        reb.save()
        rel = Death.objects.get(id=reb.death_id)
        rel.certificate = certificate
        rel.status = 'approved'
        rel.save()
        messages.info(request, " approved")

    return render(request, 'registrar/regdeath.html', {"res": res})


def statusdeath(request):
    uid = request.session['uid']
    print(uid)
    result = Death.objects.filter(user_id__user_id=uid, status='approved')
    res = Death.objects.filter(user_id__user_id=uid, status='pending')
    resul = Death.objects.filter(user_id__user_id=uid, status='forwarded')
    return render(request, 'user/statusdeath.html', {"res": res, "resul": resul, "result": result})


def withdrawdeath(request):
    id = request.GET.get('id')
    Death.objects.filter(id=id).delete()
    messages.info(request, " withdrawed ")

    return HttpResponseRedirect('/statusdeath')


def paymentdeath(request):
    id = request.GET.get('id')
    uid = request.session['uid']
    if request.POST:
        Death.objects.filter(user_id__user_id=uid, status='pending').update(
            payment_status='success')
        messages.info(request, "Suceess")
        return redirect('/statusdeath')

    return render(request, 'user/payment.html')

# marriage starts here$$$$$$$$$$$$$$$$$$$$$$$$$$$$


def applymarriage(request):
    uid = request.session['uid']
    uuid = Registration.objects.get(user_id=uid)
    if request.method == 'POST':
        # Process the form data
        bridename = request.POST['bridename']
        bridefather = request.POST['bridefather']
        bridemother = request.POST['bridemother']
        bridedob = request.POST['bridedob']
        brideaddress = request.POST['brideaddress']
        groomname = request.POST['groomname']
        groomfather = request.POST['groomfather']
        groommother = request.POST['groommother']
        groomdob = request.POST['groomdob']
        groomaddress = request.POST['groomaddress']
        taluk = request.POST.get('taluk')

        marriagedate = request.POST['marriagedate']

        marriageplace = request.POST['marriageplace']
        marriagetype = request.POST['marriagetype']
        relation = request.POST['relation']

        district = request.POST['district']
        address = request.POST['address']
        idproofbride = request.FILES['idproofbride']
        idproofgroom = request.FILES['idproofgroom']

        if Marriage.objects.filter(bridename=bridename, groomname=groomname, marriagedate=marriagedate).exists():
            print("already applied ")
            messages.info(request, "already applied")
        else:

            # Create a new User instance and save it
            user = Marriage(
                bridename=bridename,
                bridefather=bridefather,
                bridemother=bridemother,
                bridedob=bridedob,
                brideaddress=brideaddress,
                groomname=groomname,
                groomfather=groomfather,
                groommother=groommother,
                groomdob=groomdob,
                groomaddress=groomaddress,
                taluk=taluk,

                marriagedate=marriagedate,

                marriageplace=marriageplace,
                marriagetype=marriagetype,
                relation=relation,

                district=district,
                address=address,
                idproofbride=idproofbride,
                idproofgroom=idproofgroom,
                user=uuid
            )
        user.save()
        # Redirect to a success page or do something else
        messages.info(request, "applied for marriage certificate")
        return redirect('/paymentmarriage')
    return render(request, 'user/applymarriage.html')


def adminapplymarriage(request):
    res = Marriage.objects.filter(status='pending', payment_status='success')
    return render(request, 'admin/adminapplymarriage.html', {"res": res})


def deletemarriage(request):
    id = request.GET.get('id')
    Marriage.objects.filter(id=id).delete()
    messages.info(request, "deleted")

    return HttpResponseRedirect('/adminapplymarriage')


def forwardmarriage(request):
    id = request.GET.get('id')
    bb = Marriage.objects.get(id=id)
    res = Addauthority.objects.filter(
        district=bb.district, authority='registrar')

    return render(request, 'admin/forwardmarriage.html', {'res': res, 'bb': bb})


def assignmarriage(request):
    rid = request.GET.get('rid')
    bid = request.GET.get('bid')
    bb = Marriage.objects.get(id=bid)
    reg = Addauthority.objects.get(id=rid)
    bb.status = 'forwarded'
    bb.save()
    Assign.objects.create(marriage=bb, registrar=reg)
    return redirect('/adminapplymarriage')


def deletemarriagereg(request):
    id = request.GET.get('id')
    Marriage.objects.filter(id=id).delete()
    messages.info(request, "deleted")

    return HttpResponseRedirect('/regmarriage')


def regmarriage(request):
    uid = request.session['uid']
    uuid = Addauthority.objects.get(user_id=uid)
    res = Assign.objects.filter(
        marriage__payment_status='success', marriage__status='forwarded', registrar=uuid.id)
    if request.POST:
        certificate = request.FILES.get('certificate')
        print(certificate)
        bid = request.POST['bid']
        reb = Assign.objects.get(id=bid)
        reb.status = 'approved'
        reb.save()
        rel = Marriage.objects.get(id=reb.marriage_id)
        rel.certificate = certificate
        rel.status = 'approved'
        rel.save()
    return render(request, 'registrar/regmarriage.html', {"res": res})


def statusmarriage(request):
    uid = request.session['uid']
    print(uid)
    result = Marriage.objects.filter(user_id__user_id=uid, status='approved')
    res = Marriage.objects.filter(user_id__user_id=uid, status='pending')
    resul = Marriage.objects.filter(user_id__user_id=uid, status='forwarded')
    return render(request, 'user/statusmarriage.html', {"res": res, "resul": resul, "result": result})


def withdrawmarriage(request):
    id = request.GET.get('id')
    Marriage.objects.filter(id=id).delete()
    messages.info(request, "withdrawed")

    return HttpResponseRedirect('/statusmarriage')


def paymentmarriage(request):
    id = request.GET.get('id')
    uid = request.session['uid']
    if request.POST:
        Marriage.objects.filter(user_id__user_id=uid, status='pending').update(
            payment_status='success')
        messages.info(request, "Suceess")
        return redirect('/statusmarriage')

    return render(request, 'user/payment.html')


# license starts here$$$$$$$$$$$$$$$$$$$$

def applylicense(request):
    uid = request.session['uid']
    uuid = Registration.objects.get(user_id=uid)
    if request.method == 'POST':
        # Process the form data
        # name = request.POST['name']
        father = request.POST['father']
        mother = request.POST['mother']
        klno = request.POST['klno']

        gender = request.POST['gender']
        dob = request.POST['dob']
        place = request.POST['place']
        blood = request.POST['blood']

        district = request.POST['district']
        address = request.POST['address']
        identification = request.POST['identification']
        idproof = request.FILES['idproof']
        photo = request.FILES['photo']
        if License.objects.filter(klno=klno).exists():
            print("already applied ")
            messages.info(request, "already applied")
        else:
            # Create a new User instance and save it
            user = License(
                # name=name,
                father=father,
                mother=mother,
                gender=gender,
                klno=klno,
                dob=dob,
                place=place,
                blood=blood,
                photo=photo,
                district=district,
                address=address,
                identification=identification,
                idproof=idproof,
                user=uuid
            )
        user.save()
        messages.info(request, "applied for Driving License")
        # Redirect to a success page or do something else
        return redirect('/paymentlicense')
    return render(request, 'user/applylicense.html')


def adminapplylicense(request):
    res = License.objects.filter(status='pending', payment_status='success')
    return render(request, 'admin/adminapplylicense.html', {"res": res})


def deletelicense(request):
    id = request.GET.get('id')
    License.objects.filter(id=id).delete()
    messages.info(request, "deleted")

    return HttpResponseRedirect('/adminapplylicense')


def deletelicenserto(request):
    id = request.GET.get('id')
    License.objects.filter(id=id).delete()
    messages.info(request, "deleted")

    return HttpResponseRedirect('/rtolicense')


def forwardlicense(request):
    id = request.GET.get('id')
    License.objects.filter(id=id).update(status='forwarded')
    messages.info(request, "forwarded")

    return HttpResponseRedirect('/adminapplylicense')


def rtolicense(request):
    uid = request.session['uid']
    uuid = Addauthority.objects.get(user_id=uid)
    res = License.objects.filter(
        status='forwarded', payment_status='success', district=uuid.district)
    return render(request, 'rto/rtolicense.html', {"res": res})


def statuslicense(request):
    uid = request.session['uid']
    print(uid)
    result = License.objects.filter(user_id__user_id=uid, status='approved')
    res = License.objects.filter(user_id__user_id=uid, status='pending')
    resul = License.objects.filter(user_id__user_id=uid, status='forwarded')
    return render(request, 'user/statuslicense.html', {"res": res, "resul": resul, "result": result})


def withdrawlicense(request):
    id = request.GET.get('id')
    License.objects.filter(id=id).delete()
    messages.info(request, "withdrawed")

    return HttpResponseRedirect('/statuslicense')


def paymentlicense(request):
    id = request.GET.get('id')
    uid = request.session['uid']
    if request.POST:
        License.objects.filter(user_id__user_id=uid, status='pending').update(
            payment_status='success')
        messages.info(request, "Suceess")
        return redirect('/statuslicense')

    return render(request, 'user/payment.html')

# passport starts here$$$$$$$$$$$$$$$$$$$$$$$$$$$


def applypassport(request):
    uid = request.session['uid']
    uuid = Registration.objects.get(user_id=uid)
    if request.method == 'POST':
        # Process the form data
        # Retrieve form data
        # name = request.POST.get('name')
        father = request.POST.get('father')
        mother = request.POST.get('mother')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        place = request.POST.get('place')
        blood = request.POST.get('blood')
        district = request.POST.get('district')
        address = request.POST.get('address')
        identification = request.POST.get('identification')

        # Process uploaded files
        idproof = request.FILES.get('idproof')
        photo = request.FILES.get('photo')
        addressproof = request.FILES.get('addressproof')
        martial = request.POST.get('martial')
        if Passport.objects.filter(father=father, mother=mother, dob=dob,).exists():
            print("already applied ")
            messages.info(request, "already applied")
        else:
            # Create a new User instance and save it
            user = Passport(
                # name=name,
                father=father,
                mother=mother,
                gender=gender,
                dob=dob,
                place=place,
                blood=blood,
                martial=martial,
                district=district,
                address=address,
                identification=identification,
                idproof=idproof,
                photo=photo,
                addressproof=addressproof,
                user=uuid
            )
        user.save()
        messages.info(request, "applied for Passport")
        # Redirect to a success page or do something else
        return redirect('/paymentpassport')
    return render(request, 'user/applypassport.html')


def adminapplypassport(request):
    res = Passport.objects.filter(status='pending', payment_status='success')
    return render(request, 'admin/adminapplypassport.html', {"res": res})


def deletepassport(request):
    id = request.GET.get('id')
    Passport.objects.filter(id=id).delete()
    messages.info(request, "deleted")

    return HttpResponseRedirect('/adminapplypassport')


def deletepassportrpo(request):
    id = request.GET.get('id')
    Passport.objects.filter(id=id).delete()
    messages.info(request, "deleted")

    return HttpResponseRedirect('/rpopassport')


def forwardpassport(request):
    id = request.GET.get('id')
    Passport.objects.filter(id=id).update(status='forwarded')
    messages.info(request, "forwarded")

    return HttpResponseRedirect('/adminapplypassport')


def rpopassport(request):
    uid = request.session['uid']
    uuid = Addauthority.objects.get(user_id=uid)
    res = Passport.objects.filter(
        status='forwarded', payment_status='success', district=uuid.district)
    return render(request, 'rpo/rpopassport.html', {"res": res})


def statuspassport(request):
    uid = request.session['uid']
    print(uid)
    result = Passport.objects.filter(user_id__user_id=uid, status='approved')
    res = Passport.objects.filter(user_id__user_id=uid, status='pending')
    resul = Passport.objects.filter(user_id__user_id=uid, status='forwarded')
    return render(request, 'user/statuspassport.html', {"res": res, "resul": resul, "result": result})


def withdrawpassport(request):
    id = request.GET.get('id')
    Passport.objects.filter(id=id).delete()
    messages.info(request, "withdrawed")
    return HttpResponseRedirect('/statuspassport')


def paymentpassport(request):
    id = request.GET.get('id')
    uid = request.session['uid']
    if request.POST:
        Passport.objects.filter(user_id__user_id=uid, status='pending').update(
            payment_status='success')
        messages.info(request, "Suceess")
        return redirect('/statuspassport')

    return render(request, 'user/payment.html')

# voters starts here$$$$$$$$$$$$$$$$$$$$$$$$$$$$


def applyvoters(request):
    uid = request.session['uid']
    uuid = Registration.objects.get(user_id=uid)
    if request.method == 'POST':
        # Process the form data
        # Retrieve form data
        # name = request.POST.get('name')
        father = request.POST.get('father')
        mother = request.POST.get('mother')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        place = request.POST.get('place')
        blood = request.POST.get('blood')
        district = request.POST.get('district')
        address = request.POST.get('address')
        identification = request.POST.get('identification')

        # Process uploaded files
        idproof = request.FILES.get('idproof')
        photo = request.FILES.get('photo')
        addressproof = request.FILES.get('addressproof')
        martial = request.POST.get('martial')
        if Voters.objects.filter(father=father, mother=mother, dob=dob,).exists():
            print("already applied ")
            messages.info(request, "already applied")
        else:
            # Create a new User instance and save it
            user = Voters(
                # name=name,
                father=father,
                mother=mother,
                gender=gender,
                dob=dob,
                place=place,
                blood=blood,
                martial=martial,
                district=district,
                address=address,
                identification=identification,
                idproof=idproof,
                photo=photo,
                addressproof=addressproof,
                user=uuid
            )
        user.save()
        messages.info(request, "applied for Voters ID")

        # Redirect to a success page or do something else
        return redirect('/paymentvoters')
    return render(request, 'user/applyvoters.html')


def adminapplyvoters(request):
    res = Voters.objects.filter(status='pending', payment_status='success')
    return render(request, 'admin/adminapplyvoters.html', {"res": res})


def deletevoters(request):
    id = request.GET.get('id')
    Voters.objects.filter(id=id).delete()
    messages.info(request, "deleted")
    return HttpResponseRedirect('/adminapplyvoters')


def deletevotersec(request):
    id = request.GET.get('id')
    Voters.objects.filter(id=id).delete()
    messages.info(request, "deleted")
    return HttpResponseRedirect('/ecvoters')


def forwardvoters(request):
    id = request.GET.get('id')
    Voters.objects.filter(id=id).update(status='forwarded')
    messages.info(request, "forwarded")
    return HttpResponseRedirect('/adminapplyvoters')


def ecvoters(request):
    uid = request.session['uid']
    uuid = Addauthority.objects.get(user_id=uid)
    res = Voters.objects.filter(
        status='forwarded', payment_status='success', district=uuid.district)
    return render(request, 'ec/ecvoters.html', {"res": res})


def statusvoters(request):
    uid = request.session['uid']
    print(uid)
    result = Voters.objects.filter(user_id__user_id=uid, status='approved')
    res = Voters.objects.filter(user_id__user_id=uid, status='pending')
    resul = Voters.objects.filter(user_id__user_id=uid, status='forwarded')
    return render(request, 'user/statusvoters.html', {"res": res, "resul": resul, "result": result})


def withdrawvoters(request):
    id = request.GET.get('id')
    Voters.objects.filter(id=id).delete()
    messages.info(request, "withdrawed")
    return HttpResponseRedirect('/statusvoters')


def paymentvoters(request):
    id = request.GET.get('id')
    uid = request.session['uid']
    if request.POST:
        Voters.objects.filter(user_id__user_id=uid, status='pending').update(
            payment_status='success')
        messages.info(request, "Suceess")
        return redirect('/statusvoters')
    return render(request, 'user/payment.html')

# feedback starts here$$$$$$$$$$$$$$$$$$$$$$$$$$$$


def addfeedback(request):
    uid = request.session['uid']
    uuid = Registration.objects.get(user_id=uid)
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        user = Feedback(
            feedback=feedback,
            user=uuid
        )
        user.save()
        messages.info(request, "feedback added")
    return render(request, 'user/addfeedback.html')


def viewfeedback(request):
    res = Feedback.objects.all()
    return render(request, 'admin/viewfeedback.html', {"res": res})
# help starts here$$$$$$$$$$$$$$$$$$$$$$$$$$$$


def help(request):
    return render(request, 'user/help.html')


def approvevoters(request):
    vid = request.GET.get('id')
    voter = Voters.objects.get(id=vid)
    voter.status = 'approved'
    voter.save()
    return redirect('/ecvoters')

