from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib import messages
from httpx import request
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


from django.utils.crypto import get_random_string

##################### admin ######################
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.shortcuts import render, redirect

def addauthority(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        district = request.POST.get('district')
        authority = request.POST.get('authority')

        # ✅ Email validation
        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return redirect('addauthority')

        # ✅ Phone validation
        if not phone_number.isdigit() or len(phone_number) != 10:
            messages.error(request, "Invalid phone number")
            return redirect('addauthority')

        # ✅ Authority check
        if Addauthority.objects.filter(district=district, authority=authority).exists():
            messages.error(request, "Authority already exists in this district")
            return redirect('addauthority')

        # ✅ Generate password
        password = get_random_string(length=10)

        # ✅ Create user
        loginqry = Login.objects.create_user(
            username=email,
            password=password,
            viewpassword=password,
            usertype=authority
        )

        # ✅ Create authority
        Addauthority.objects.create(
            name=name,
            email=email,
            password=password,
            phone_number=phone_number,
            district=district,
            authority=authority,
            user=loginqry
        )

        # ✅ Send email
        subject = "Your Account Created"
        message = f"""
Hello {name},

Your account has been created successfully.

Login Details:
Email: {email}
Password: {password}

Please change your password after login.

Thank you.
"""
        send_mail(subject, message, None, [email])

        messages.success(request, "Authority registered & password sent to email")
        return redirect('/viewauthority')

    return render(request, 'admin/addauthority.html')


from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

def addregistrar(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        taluk = request.POST.get('taluk')
        phone_number = request.POST.get('phone')
        district = request.POST.get('district')

        # ✅ Email validation
        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email already in use")
            return redirect('addregistrar')

        # ✅ Phone validation
        if not phone_number.isdigit() or len(phone_number) != 10:
            messages.error(request, "Invalid phone number")
            return redirect('addregistrar')

        # ✅ Registrar existence check (before creating user)
        if Addauthority.objects.filter(taluk=taluk, district=district, authority='registrar').exists():
            messages.error(request, "Registrar already exists in this area")
            return redirect('addregistrar')

        # ✅ Generate password automatically
        password = get_random_string(length=10)

        # ✅ Create user
        loginqry = Login.objects.create_user(
            username=email,
            password=password,
            viewpassword=password,  # ⚠️ better remove later
            usertype='registrar'
        )

        # ✅ Create registrar
        Addauthority.objects.create(
            name=name,
            email=email,
            taluk=taluk,
            password=password,
            phone_number=phone_number,
            district=district,
            authority='registrar',
            user=loginqry
        )

        # ✅ Send email
        subject = "Registrar Account Created"
        message = f"""
Hello {name},

Your Registrar account has been created successfully.

Login Details:
Email: {email}
Password: {password}

Please login and change your password immediately.

Thank you.
"""
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

        messages.success(request, "Registrar added & password sent to email")
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

from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings

def applybirth(request):
    uid = request.session['uid']
    uuid = Registration.objects.get(user_id=uid)

    if request.method == 'POST':
        name = request.POST['name']
        father = request.POST['father']
        mother = request.POST['mother']

        father_phone = request.POST['father_phone']
        mother_phone = request.POST['mother_phone']

        father_email = request.POST['father_email']
        mother_email = request.POST['mother_email']

        father_address = request.POST['father_address']
        mother_address = request.POST['mother_address']

        father_blood = request.POST['father_blood']
        mother_blood = request.POST['mother_blood']
        child_blood = request.POST['child_blood']

        father_idproof = request.FILES['father_idproof']
        mother_idproof = request.FILES['mother_idproof']

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

        # ✅ OTP GENERATION
        otp = get_random_string(length=6, allowed_chars='0123456789')

        birth_obj = Birth.objects.create(
            name=name,
            father=father,
            mother=mother,

            father_phone=father_phone,
            mother_phone=mother_phone,

            father_email=father_email,
            mother_email=mother_email,

            father_address=father_address,
            mother_address=mother_address,

            father_blood=father_blood,
            mother_blood=mother_blood,
            child_blood=child_blood,

            father_idproof=father_idproof,
            mother_idproof=mother_idproof,

            gender=gender,
            dob=dob,
            birthplace=birthplace,
            birth=birth,
            relation=relation,
            taluk=taluk,
            district=district,
            address=address,
            identification=identification,
            idproof=idproof,
            user=uuid,
            otp=otp
        )

        # ✅ SEND OTP TO USER EMAIL
        send_mail(
            "OTP Verification",
            f"Your OTP is: {otp}",
            settings.EMAIL_HOST_USER,
            [uuid.email]
        )

        return redirect(f'/verify-otp/{birth_obj.id}')

    return render(request, 'user/applybirth.html')


def verify_otp(request, id):
    birth = Birth.objects.get(id=id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if birth.otp == entered_otp:
            birth.is_verified = True
            birth.save()

            messages.success(request, "OTP Verified Successfully")
            return redirect('/paymentbirth')

        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'user/verify_otp.html', {'birth': birth})

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

    assign = Assign.objects.get(id=id)
    birth = assign.birth

    # Update status instead of hard delete (recommended)
    assign.status = 'rejected'
    birth.status = 'rejected'

    assign.save()
    birth.save()

    messages.error(request, "Application Rejected")

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


from django.utils import timezone
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.core.files.base import ContentFile
import io
import io
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.core.files.base import ContentFile


def regbirth(request):
    uid = request.session['uid']
    uuid = Addauthority.objects.get(user_id=uid)

    res = Assign.objects.filter(
        birth__payment_status='success',
        birth__status='forwarded',
        registrar=uuid.id
    )

    if request.method == 'POST':
        bid = request.POST.get('bid')
        action = request.POST.get('action')

        assign = Assign.objects.get(id=bid)
        birth = assign.birth

        # ✅ APPROVE → Generate PDF
        if action == "approve":

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer)

            styles = getSampleStyleSheet()
            content = []

            content.append(Paragraph("<b>Birth Certificate</b>", styles['Title']))
            content.append(Spacer(1, 10))

            content.append(Paragraph(f"Name: {birth.name}", styles['Normal']))
            content.append(Paragraph(f"Father: {birth.father}", styles['Normal']))
            content.append(Paragraph(f"Mother: {birth.mother}", styles['Normal']))
            content.append(Paragraph(f"DOB: {birth.dob}", styles['Normal']))
            content.append(Paragraph(f"Gender: {birth.gender}", styles['Normal']))
            content.append(Paragraph(f"Birth Place: {birth.birthplace}", styles['Normal']))
            content.append(Paragraph(f"District: {birth.district}", styles['Normal']))

            content.append(Spacer(1, 20))
            content.append(Paragraph(f"Date of Issue: {timezone.now().date()}", styles['Normal']))

            content.append(Spacer(1, 30))
            content.append(Paragraph(f"Registrar Signature: {uuid.name}", styles['Normal']))

            doc.build(content)

            pdf = buffer.getvalue()
            buffer.close()

            filename = f"birth_{birth.id}.pdf"
            birth.certificate.save(filename, ContentFile(pdf))

            birth.status = 'approved'
            assign.status = 'approved'

            birth.save()
            assign.save()

            messages.success(request, "Birth Certificate Generated & Approved")

        return redirect('/regbirth')

    return render(request, 'registrar/regbirth.html', {"res": res})


# ✅ REJECT (NO DELETE - safer)
def deletebirthreg(request):
    id = request.GET.get('id')

    assign = Assign.objects.get(id=id)
    birth = assign.birth

    assign.status = 'rejected'
    birth.status = 'rejected'

    assign.save()
    birth.save()

    messages.error(request, "Application Rejected")

    return HttpResponseRedirect('/regbirth')

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

import datetime
from django.contrib import messages
from django.shortcuts import render, redirect

def paymentbirth(request):
    uid = request.session.get('uid')

    if not uid:
        messages.error(request, "Login required")
        return redirect('/')

    birth = Birth.objects.filter(user_id__user_id=uid, status='pending').first()

    # ✅ OTP check
    if not birth or not birth.is_verified:
        messages.error(request, "Verify OTP first")
        return redirect('/')

    if request.method == 'POST':
        name = request.POST.get('name')
        card_number = request.POST.get('number')
        cvv = request.POST.get('cvv')
        expiry = request.POST.get('expiry')

        # ✅ Card number validation (16 digits)
        if not card_number.isdigit() or len(card_number) != 16:
            messages.error(request, "Invalid card number (must be 16 digits)")
            return redirect('/paymentbirth')

        # ✅ CVV validation (3 digits only)
        if not cvv.isdigit() or len(cvv) != 3:
            messages.error(request, "Invalid CVV (must be 3 digits)")
            return redirect('/paymentbirth')

        # ✅ Expiry validation (future date only)
        try:
            exp_date = datetime.datetime.strptime(expiry, "%Y-%m").date()
            today = datetime.date.today().replace(day=1)

            if exp_date < today:
                messages.error(request, "Card expired")
                return redirect('/paymentbirth')

        except:
            messages.error(request, "Invalid expiry date")
            return redirect('/paymentbirth')

        # ✅ Payment success (dummy)
        birth.payment_status = 'success'
        birth.save()

        messages.success(request, "Payment Successful")
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

        father_address = request.POST['father_address']
        father_phone = request.POST['father_phone']
        father_email = request.POST['father_email']
        father_blood = request.POST['father_blood']
        father_idproof = request.FILES.get('father_idproof')

        mother_address = request.POST['mother_address']
        mother_phone = request.POST['mother_phone']
        mother_email = request.POST['mother_email']
        mother_blood = request.POST['mother_blood']
        mother_idproof = request.FILES.get('mother_idproof')

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

        # ✅ OTP GENERATION
        otp = get_random_string(length=6, allowed_chars='0123456789')

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
                user=uuid,
                father_address=father_address,
                mother_address=mother_address,
                father_phone=father_phone,
                mother_phone=mother_phone,
                father_email=father_email,
                mother_email=mother_email,
                father_blood=father_blood,
                mother_blood=mother_blood,
                father_idproof=father_idproof,
                mother_idproof=mother_idproof,
                otp=otp

            )
        user.save()

        # ✅ SEND OTP TO USER EMAIL
        send_mail(
            "OTP Verification",
            f"Your OTP is: {otp}",
            settings.EMAIL_HOST_USER,
            [uuid.email]
        )

        return redirect(f'/verify-otpDeath/{user.id}')
        messages.info(request, " applied for death certificate ")
        # Redirect to a success page or do something else
        return redirect('/paymentdeath')
    return render(request, 'user/applydeath.html')


def verify_otpDeath(request, id):
    death = Death.objects.get(id=id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if death.otp == entered_otp:
            death.is_verified = True
            death.save()

            messages.success(request, "OTP Verified Successfully")
            return redirect('/paymentdeath')

        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'user/verify_otpDeath.html', {'death': death})



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


from django.utils import timezone
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.core.files.base import ContentFile
import io

def regdeath(request):
    uid = request.session['uid']
    uuid = Addauthority.objects.get(user_id=uid)

    res = Assign.objects.filter(
        death__payment_status='success',
        death__status='forwarded',
        registrar=uuid.id
    )

    if request.method == 'POST':
        bid = request.POST.get('bid')
        action = request.POST.get('action')

        assign = Assign.objects.get(id=bid)
        death = assign.death

        # ✅ APPROVE → generate PDF
        if action == "approve":

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer)

            styles = getSampleStyleSheet()
            content = []

            content.append(Paragraph("<b>Death Certificate</b>", styles['Title']))
            content.append(Spacer(1, 10))

            content.append(Paragraph(f"Name: {death.name}", styles['Normal']))
            content.append(Paragraph(f"Father: {death.father}", styles['Normal']))
            content.append(Paragraph(f"Mother: {death.mother}", styles['Normal']))
            content.append(Paragraph(f"DOB: {death.dob}", styles['Normal']))
            content.append(Paragraph(f"Date of Death: {death.dod}", styles['Normal']))
            content.append(Paragraph(f"Place of Death: {death.deathplace}", styles['Normal']))
            content.append(Paragraph(f"District: {death.district}", styles['Normal']))

            content.append(Spacer(1, 20))
            content.append(Paragraph(
                f"Issue Date: {timezone.now().date()}",
                styles['Normal']
            ))

            content.append(Spacer(1, 30))
            content.append(Paragraph(
                f"Registrar Signature: {uuid.name}",
                styles['Normal']
            ))

            doc.build(content)

            pdf = buffer.getvalue()
            buffer.close()

            filename = f"death_{death.id}.pdf"
            death.certificate.save(filename, ContentFile(pdf))

            death.status = 'approved'
            assign.status = 'approved'

            death.save()
            assign.save()

            messages.success(request, "Death Certificate Generated")

        return redirect('/regdeath')

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

        otp = get_random_string(length=6, allowed_chars='0123456789')

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
                user=uuid,
                otp=otp
            )
        user.save()
        # Redirect to a success page or do something else
        messages.info(request, "applied for marriage certificate")
         # ✅ SEND OTP TO USER EMAIL
        send_mail(
            "OTP Verification",
            f"Your OTP is: {otp}",
            settings.EMAIL_HOST_USER,
            [uuid.email]
        )

        return redirect(f'/verify-otpMarriage/{user.id}')
        return redirect('/paymentmarriage')
    return render(request, 'user/applymarriage.html')

def verify_otpMarriage(request, id):
    marriage = Marriage.objects.get(id=id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if marriage.otp == entered_otp:
            marriage.is_verified = True
            marriage.save()

            messages.success(request, "OTP Verified Successfully")
            return redirect('/paymentmarriage')

        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'user/verify_otpMarriage.html', {'marriage': marriage})


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



from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from django.conf import settings
from datetime import date
def generate_marriage_certificate(data, registrar):
    filename = f"marriage_{data.id}.pdf"
    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    doc = SimpleDocTemplate(filepath)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b>MARRIAGE CERTIFICATE</b>", styles['Title']))
    content.append(Spacer(1, 20))

    content.append(Paragraph(f"<b>Bride Name:</b> {data.bridename}", styles['Normal']))
    content.append(Paragraph(f"<b>Groom Name:</b> {data.groomname}", styles['Normal']))
    content.append(Paragraph(f"<b>Marriage Date:</b> {data.marriagedate}", styles['Normal']))
    content.append(Paragraph(f"<b>Place:</b> {data.marriageplace}", styles['Normal']))
    content.append(Paragraph(f"<b>District:</b> {data.district}", styles['Normal']))

    content.append(Spacer(1, 20))
    content.append(Paragraph(f"<b>Issued Date:</b> {date.today()}", styles['Normal']))

    content.append(Spacer(1, 40))

    # ✅ Registrar Name as Signature
    content.append(Paragraph(f"<b>Registrar:</b> {registrar.name}", styles['Normal']))
    content.append(Paragraph(f"<b>Authority:</b> {registrar.authority}", styles['Normal']))

    content.append(Spacer(1, 10))
    content.append(Paragraph("Digital Signature", styles['Italic']))

    doc.build(content)

    return filename


def regmarriage(request):
    uid = request.session['uid']
    uuid = Addauthority.objects.get(user_id=uid)

    res = Assign.objects.filter(
        marriage__payment_status='success',
        marriage__status='forwarded',
        registrar=uuid.id
    )

    if request.method == 'POST':
        bid = request.POST['bid']

        assign = Assign.objects.get(id=bid)
        marriage = Marriage.objects.get(id=assign.marriage_id)

        # Generate PDF
        filename = generate_marriage_certificate(marriage)

        # Update records
        marriage.certificate = filename
        marriage.status = 'approved'
        marriage.save()

        assign.status = 'approved'
        assign.save()

        messages.success(request, "Approved & Certificate Generated")

        return redirect('/regmarriage')

    return render(request, 'registrar/regmarriage.html', {"res": res})


def deletemarriagereg(request):
    id = request.GET.get('id')

    Assign.objects.filter(id=id).delete()

    messages.info(request, "Rejected")
    return HttpResponseRedirect('/regmarriage')



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

        father_phone = request.POST['father_phone']
        father_email = request.POST['father_email']
        father_address = request.POST['father_address']
        father_proof = request.FILES['father_proof']

        mother_phone = request.POST['mother_phone']
        mother_email = request.POST['mother_email']
        mother_address = request.POST['mother_address']
        mother_proof = request.FILES['mother_proof']



        gender = request.POST['gender']
        dob = request.POST['dob']
        place = request.POST['place']
        blood = request.POST['blood']
        name=request.POST['name']
        district = request.POST['district']
        address = request.POST['address']
        identification = request.POST['identification']
        idproof = request.FILES['idproof']
        photo = request.FILES['photo']

        otp = get_random_string(length=6, allowed_chars='0123456789')

        if License.objects.filter(klno=klno).exists():
            print("already applied ")
            messages.info(request, "already applied")
        else:
            # Create a new User instance and save it
            user = License(
                name=name,
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
                user=uuid,

                father_phone=father_phone,
                father_email=father_email,
                father_address=father_address,
                father_proof=father_proof,
                mother_phone = mother_phone,
                mother_email = mother_email,
                mother_address = mother_address,
                mother_proof = mother_proof,
                otp=otp

            )
        user.save()
        messages.info(request, "applied for Driving License")

        # ✅ SEND OTP TO USER EMAIL
        send_mail(
            "OTP Verification",
            f"Your OTP is: {otp}",
            settings.EMAIL_HOST_USER,
            [uuid.email]
        )

        return redirect(f'/verify-otpLisence/{user.id}')

        # Redirect to a success page or do something else
        return redirect('/paymentlicense')
    return render(request, 'user/applylicense.html')

def verify_otpLisence(request, id):
    license = License.objects.get(id=id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if license.otp == entered_otp:
            license.is_verified = True
            license.save()

            messages.success(request, "OTP Verified Successfully")
            return redirect('/paymentlicense')

        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'user/verify_otpLicense.html', {'license': license})


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

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import date
def approvelicense(request):
    lid = request.GET.get('id')
    lic = License.objects.get(id=lid)

    lic.status = 'approved'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "DRIVING LICENSE CERTIFICATE")

    p.setFont("Helvetica", 12)
    p.drawString(50, 750, f"Name: {lic.name}")
    p.drawString(50, 730, f"Father: {lic.father}")
    p.drawString(50, 710, f"Mother: {lic.mother}")
    p.drawString(50, 690, f"DOB: {lic.dob}")
    p.drawString(50, 670, f"District: {lic.district}")
    p.drawString(50, 650, f"KL Number: {lic.klno}")

    # ✅ FIXED LINE (IMPORTANT)
    registrar = Addauthority.objects.get(user_id=request.session['uid'])

    p.drawString(50, 600, f"Issued by: {registrar.name}")
    p.drawString(50, 580, f"Date: {date.today()}")

    p.showPage()
    p.save()

    buffer.seek(0)

    filename = f"license_{lic.id}.pdf"
    lic.certificate.save(filename, buffer)

    lic.save()

    messages.info(request, "License Approved & PDF Generated")

    return redirect('/rtolicense')


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

        name = request.POST.get('name')
        father = request.POST.get('father')
        mother = request.POST.get('mother')
        dob = request.POST.get('dob')

        if Passport.objects.filter(father=father, mother=mother, dob=dob).exists():
            messages.info(request, "already applied")
            return redirect('/applypassport')

        passport = Passport(
            name=name,   # ✅ THIS WILL NOW SAVE PROPERLY
            father=father,
            mother=mother,
            gender=request.POST.get('gender'),
            dob=dob,
            place=request.POST.get('place'),
            blood=request.POST.get('blood'),
            martial=request.POST.get('martial'),
            district=request.POST.get('district'),
            address=request.POST.get('address'),
            identification=request.POST.get('identification'),

            idproof=request.FILES.get('idproof'),
            photo=request.FILES.get('photo'),
            addressproof=request.FILES.get('addressproof'),

            user=uuid,

            father_email=request.POST.get('father_email'),
            father_phone=request.POST.get('father_phone'),
            father_address=request.POST.get('father_address'),
            father_proof=request.FILES.get('father_proof'),

            mother_email=request.POST.get('mother_email'),
            mother_phone=request.POST.get('mother_phone'),
            mother_address=request.POST.get('mother_address'),
            mother_proof=request.FILES.get('mother_proof'),

            otp=get_random_string(length=6, allowed_chars='0123456789')
        )

        passport.save()

        messages.info(request, "applied for Passport")

        send_mail(
            "OTP Verification",
            f"Your OTP is: {passport.otp}",
            settings.EMAIL_HOST_USER,
            [uuid.email]
        )

        return redirect(f'/verify-otpPassport/{passport.id}')


def verify_otpPassport(request, id):
    passport = Passport.objects.get(id=id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if passport.otp == entered_otp:
            passport.is_verified = True
            passport.save()

            messages.success(request, "OTP Verified Successfully")
            return redirect('/paymentpassport')

        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'user/verify_otpPassport.html', {'passport': passport})



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
        status='forwarded',
        payment_status='success',
        district=uuid.district
    )

    return render(request, 'rpo/rpopassport.html', {"res": res})

from django.http import HttpResponse, HttpResponseRedirect
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import date
from django.contrib import messages

def approvepassport(request):
    pid = request.GET.get('id')
    passport = Passport.objects.get(id=pid)

    passport.status = 'approved'

    # ================= PDF GENERATION =================
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, 800, "PASSPORT CERTIFICATE")

    p.setFont("Helvetica", 12)

    # Basic details
    p.drawString(50, 760, f"Name: {passport.name}")
    p.drawString(50, 740, f"Father: {passport.father}")
    p.drawString(50, 720, f"Mother: {passport.mother}")
    p.drawString(50, 700, f"DOB: {passport.dob}")
    p.drawString(50, 680, f"Gender: {passport.gender}")
    p.drawString(50, 660, f"Place: {passport.place}")
    p.drawString(50, 640, f"District: {passport.district}")
    p.drawString(50, 620, f"Address: {passport.address}")

    # Applicant
    p.drawString(50, 590, f"Applicant: {passport.user.name}")
    p.drawString(50, 570, f"Phone: {passport.user.phone_number}")
    p.drawString(50, 550, f"Aadhar: {passport.user.aadhar}")

    # Issuer (signature from Addauthority)
    registrar = Addauthority.objects.get(user_id=request.session['uid'])
    p.drawString(50, 520, f"Issued By: {registrar.name}")

    # Date
    p.drawString(50, 500, f"Date: {date.today()}")

    p.showPage()
    p.save()

    buffer.seek(0)

    filename = f"passport_{passport.id}.pdf"
    passport.certificate.save(filename, buffer)

    passport.save()

    messages.info(request, "Passport Approved & PDF Generated")

    return HttpResponseRedirect('/rpopassport')


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

        name = request.POST.get('name')
        father = request.POST.get('father')
        mother = request.POST.get('mother')

        father_email = request.POST.get('father_email')
        father_phone = request.POST.get('father_phone')
        father_address = request.POST.get('father_address')
        father_proof = request.FILES.get('father_proof')

        mother_email = request.POST.get('mother_email')
        mother_phone = request.POST.get('mother_phone')
        mother_address = request.POST.get('mother_address')
        mother_proof = request.FILES.get('mother_proof')

        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        place = request.POST.get('place')
        blood = request.POST.get('blood')
        district = request.POST.get('district')
        address = request.POST.get('address')
        identification = request.POST.get('identification')

        idproof = request.FILES.get('idproof')
        photo = request.FILES.get('photo')
        addressproof = request.FILES.get('addressproof')
        martial = request.POST.get('martial')

        otp = get_random_string(length=6, allowed_chars='0123456789')

        # check duplicate
        if Voters.objects.filter(father=father, mother=mother, dob=dob).exists():
            messages.info(request, "already applied")
            return redirect('/applyvoters')

        # ✅ SAVE CORRECTLY
        voter = Voters.objects.create(
            name=name,
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
            user=uuid,

            father_email=father_email,
            father_phone=father_phone,
            father_address=father_address,
            father_proof=father_proof,

            mother_email=mother_email,
            mother_phone=mother_phone,
            mother_address=mother_address,
            mother_proof=mother_proof,

            otp=otp
        )

        messages.info(request, "applied for Voters ID")

        send_mail(
            "OTP Verification",
            f"Your OTP is: {otp}",
            settings.EMAIL_HOST_USER,
            [uuid.email]
        )

        return redirect(f'/verify-otpVotter/{voter.id}')

    return render(request, 'user/applyvoters.html')


def verify_otpVotter(request, id):
    voter = Voters.objects.get(id=id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if voter.otp == entered_otp:
            voter.is_verified = True
            voter.save()

            messages.success(request, "OTP Verified Successfully")
            return redirect('/paymentvoters')

        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'user/verify_otpVotter.html', {'voter': voter})


def adminapplyvoters(request):
    res = Voters.objects.filter(status='pending', payment_status='success')
    return render(request, 'admin/adminapplyvoters.html', {"res": res})


def deletevoters(request):
    id = request.GET.get('id')
    Voters.objects.filter(id=id).delete()
    messages.info(request, "deleted")
    return HttpResponseRedirect('/adminapplyvoters')




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

from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from datetime import date
from django.shortcuts import redirect

def approvevoters(request):
    vid = request.GET.get('id')
    voter = Voters.objects.get(id=vid)

    voter.status = "approved"

    # ================= PDF GENERATION =================
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, 800, "VOTER ID CERTIFICATE")

    p.setFont("Helvetica", 12)

    y = 750
    p.drawString(50, y, f"Name: {voter.name}")
    y -= 20
    p.drawString(50, y, f"Father: {voter.father}")
    y -= 20
    p.drawString(50, y, f"Mother: {voter.mother}")
    y -= 20
    p.drawString(50, y, f"DOB: {voter.dob}")
    y -= 20
    p.drawString(50, y, f"District: {voter.district}")
    y -= 20
    p.drawString(50, y, f"Address: {voter.address}")

    # ✅ EC SIGNATURE (IMPORTANT FIX)
    ec = Addauthority.objects.get(user_id=request.session['uid'])
    y -= 40
    p.drawString(50, y, f"Issued By (EC): {ec.name}")

    y -= 20
    p.drawString(50, y, f"Date: {date.today()}")

    p.showPage()
    p.save()

    buffer.seek(0)

    filename = f"voter_{voter.id}.pdf"
    voter.certificate.save(filename, buffer)

    voter.save()

    return redirect('/ecvoters')

def deletevotersec(request):
    id = request.GET.get('id')
    Voters.objects.filter(id=id).delete()
    messages.info(request, "deleted")
    return HttpResponseRedirect('/ecvoters')


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





from django.shortcuts import render, redirect
from django.contrib import messages

def user_profile(request):
    uid = request.session.get('uid')

    if not uid:
        messages.error(request, "Login required")
        return redirect('/')

    try:
        user_login = Login.objects.get(id=uid)
        user_reg = Registration.objects.get(user=user_login)
    except:
        messages.error(request, "User not found")
        return redirect('/')

    return render(request, 'user/user_profile.html', {
        'login': user_login,
        'user': user_reg
    })


from django.shortcuts import render, redirect
from django.contrib import messages

def authority_profile(request):
    uid = request.session.get('uid')

    if not uid:
        messages.error(request, "Login required")
        return redirect('/')

    try:
        login = Login.objects.get(id=uid)
        authority = Addauthority.objects.get(user=login)
    except:
        messages.error(request, "Authority not found")
        return redirect('/')

    # 🔥 Dynamic template selection
    if login.usertype == 'rto':
        template = 'rto/authority_profile.html'
    elif login.usertype == 'rpo':
        template = 'rpo/authority_profile.html'
    elif login.usertype == 'registrar':
        template = 'registrar/authority_profile.html'
    elif login.usertype == 'election':
        template = 'ec/authority_profile.html'
    else:
        messages.error(request, "Invalid user type")
        return redirect('/')

    return render(request, template, {
        'login': login,
        'auth': authority
    })