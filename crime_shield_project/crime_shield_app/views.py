from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
import re
from django.contrib.auth.hashers import make_password


# Create your views here.
# def adm(request):
#     adm=Login.objects.create_superuser(username='admin',email='admin@gmail.com',viewpassword='1234',password='1234',usertype='Admin')
#     adm.save()
#     return redirect('/')

def dlt(request):
    Login.objects.filter(id="1").delete()
    return redirect('/')

def index(request):
    return render(request,'index.html')

def logins(request):
    return render(request,'login.html')


def view_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']       
        user = authenticate(request, username=username, password=password) 

        if user is not None:
            if user.is_active:
                auth_login(request, user)  

                if user.usertype == "Admin":
                    messages.success(request, 'Welcome as Admin')
                    return redirect('admin_dashboard')

                elif user.usertype == "User":
                    request.session['uid'] = user.id
                    messages.success(request, 'Welcome as User')
                    return redirect('user_dashboard')
                
                elif user.usertype == "Police Department":
                    request.session['uid'] = user.id
                    messages.success(request, 'Welcome as Police Drepartment')
                    return redirect('police_department_dashboard')
                
                else:
                    return redirect('logins')  
            else:
                messages.error(request, 'Your account is inactive')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


# def admin_dashboard(request):
#         return render(request, 'admin/admin_dashboard.html')
    
def user_dashboard(request):
        return render(request, 'user/user_dashboard.html')

def police_department_dashboard(request):
        return render(request, 'police/police_department_dashboard.html')


def police_department_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        image = request.FILES.get("image")

        email_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
        domain_pattern = r".+\.(in|com)$"
        phone_pattern = r"^\d{10}$"

        if not re.match(email_pattern, email):
            messages.error(request, "Only Gmail addresses are allowed.")
            return redirect("police_department_register")

        if not re.match(domain_pattern, email):
            messages.error(request, "Email must have a .in or .com domain.")
            return redirect("police_department_register")

        if not re.match(phone_pattern, phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect("police_department_register")

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect("police_department_register")

        if Login.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect("police_department_register")

        if Police_department.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number is already registered.")
            return redirect("police_department_register")

        login_user = Login.objects.create(
            username=username,
            password=make_password(password),
            usertype="Police Department",
            email=email,
            viewpassword=password,
        )

        Police_department.objects.create(
            user=login_user,
            username=username,
            name=name,
            address=address,
            phone=phone,
            email=email,
            image=image
        )

        messages.success(request, "Police department registered successfully!")
        return redirect("view_login")

    return render(request, "police_department_register.html")


def user_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        image = request.FILES.get("image")

        email_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
        domain_pattern = r".+\.(in|com)$"
        phone_pattern = r"^\d{10}$"

        if not re.match(email_pattern, email):
            messages.error(request, "Only Gmail addresses are allowed.")
            return redirect("user_register")

        if not re.match(domain_pattern, email):
            messages.error(request, "Email must have a .in or .com domain.")
            return redirect("user_register")

        if not re.match(phone_pattern, phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect("user_register")

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect("user_register")

        if Login.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect("user_register")

        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number is already registered.")
            return redirect("user_register")

        login_user = Login.objects.create(
            username=username,
            password=make_password(password),
            usertype="User",
            email=email,
            viewpassword=password,
        )

        User.objects.create(
            user=login_user,
            username=username,
            name=name,
            address=address,
            phone=phone,
            email=email,
            image=image
        )

        messages.success(request, "User registered successfully!")
        return redirect("view_login")

    return render(request, "user_register.html")



def add_law(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']

        police_user = Police_department.objects.get(user=request.user)
        Law.objects.create(police=police_user, title=title, description=description)

        messages.success(request, "Law added successfully.")
        return redirect('add_law')

    return render(request, 'police/add_law.html')


def view_laws(request):
    police = Police_department.objects.get(user=request.user)
    laws = Law.objects.filter(police=police)
    return render(request, 'police/view_laws.html', {'laws': laws})


def user_view_laws(request):
    laws = Law.objects.all().order_by('-date_added')
    return render(request, 'user/user_view_laws.html', {'laws': laws})


def user_register_complaint(request):
    user = User.objects.get(user=request.user)
    departments = Police_department.objects.all()

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        department_id = request.POST['department']
        file = request.FILES.get('file')

        department = Police_department.objects.get(id=department_id)

        Complaint.objects.create(
            user=user,
            department=department,
            title=title,
            description=description,
            file=file
        )

        messages.success(request, 'Complaint submitted successfully!')
        return redirect('user_register_complaint')

    return render(request, 'user/user_register_complaint.html', {'departments': departments})


def user_view_complaints(request):
    logged_user = User.objects.get(user=request.user)
    complaints = Complaint.objects.filter(user=logged_user).order_by('-date_submitted')
    return render(request, 'user/user_view_complaints.html', {'complaints': complaints})


def police_view_complaints(request):
    police = Police_department.objects.get(user=request.user)
    complaints = Complaint.objects.filter(department=police).order_by('-date_submitted')
    return render(request, 'police/police_view_complaints.html', {'complaints': complaints})


def update_complaint_status(request, complaint_id):
    if request.method == 'POST':
        new_status = request.POST['status']
        complaint = Complaint.objects.get(id=complaint_id)
        complaint.status = new_status
        complaint.save()
    return redirect('police_view_complaints')


def add_case_report(request, complaint_id):
    police = Police_department.objects.get(user=request.user)
    complaint = Complaint.objects.get(id=complaint_id)

    if request.method == 'POST':
        case_evidence = request.POST['case_evidence']
        description = request.POST['description']
        report_file = request.FILES.get('report_file')

        CaseReport.objects.create(
            complaint=complaint,
            police=police,
            case_evidence=case_evidence,
            description=description,
            report_file=report_file
        )

        complaint.status = 'Resolved'
        complaint.save()

        return redirect('police_view_complaints')
    
    return render(request, 'police/add_case_report.html', {'complaint': complaint})


def view_case_report(request, complaint_id):
    police = Police_department.objects.get(user=request.user)
    complaint = Complaint.objects.get(id=complaint_id)
    report = CaseReport.objects.get(complaint=complaint, police=police)
    return render(request, 'police/view_case_report.html', {'report': report, 'complaint': complaint})

def user_case_reports(request):
    login_user = Login.objects.get(id=request.user.id)
    user = User.objects.get(user=login_user)
    complaints = Complaint.objects.filter(user=user, status='Resolved')
    reports = CaseReport.objects.filter(complaint__in=complaints)
    return render(request, 'user/user_case_reports.html', {'reports': reports})



############################# Missing Person Reporting ###############################

def report_missing_person(request):
    login_user = Login.objects.get(id=request.user.id)
    user = User.objects.get(user=login_user)
    departments = Police_department.objects.all()

    if request.method == 'POST':
        person_name = request.POST['person_name']
        age = request.POST['age']
        last_seen_location = request.POST['last_seen_location']
        address = request.POST['address']
        pincode = request.POST['pincode']
        description = request.POST['description']
        department_id = request.POST['department']
        department = Police_department.objects.get(id=department_id)
        photo = request.FILES.get('photo')

        MissingPerson.objects.create(
            user=user,
            department=department,
            person_name=person_name,
            age=age,
            last_seen_location=last_seen_location,
            address=address,
            pincode=pincode,
            description=description,
            photo=photo
        )
        return redirect('my_missing_cases')  # Replace with your user homepage URL name

    return render(request, 'user/report_missing_person.html', {'departments': departments})


def my_missing_cases(request):
    login_user = Login.objects.get(id=request.user.id)
    user = User.objects.get(user=login_user)
    cases = MissingPerson.objects.filter(user=user).order_by('-date_reported')
    return render(request, 'user/my_missing_cases.html', {'cases': cases})


def police_missing_cases(request):
    police = Police_department.objects.get(user=request.user)
    cases = MissingPerson.objects.filter(department=police)
    return render(request, 'police/police_missing_cases.html', {'cases': cases})


def update_missing_status(request, missing_id):
    if request.method == 'POST':
        new_status = request.POST['status']
        missing_case = MissingPerson.objects.get(id=missing_id)
        missing_case.status = new_status
        missing_case.save()
        messages.success(request, 'Missing person case status updated successfully.')
    return redirect('police_missing_cases')


def add_report_missing(request, missing_id):
    police = Police_department.objects.get(user=request.user)
    missing = MissingPerson.objects.get(id=missing_id)

    if request.method == 'POST':
        case_evidence = request.POST['case_evidence']
        description = request.POST['description']
        report_file = request.FILES.get('report_file')

        CaseReport.objects.create(
            missing_person=missing,
            police=police,
            case_evidence=case_evidence,
            description=description,
            report_file=report_file
        )

        missing.status = 'Resolved'
        missing.save()
        messages.success(request, 'Missing person case reported successfully.')
        return redirect('police_missing_cases')

    return render(request, 'police/add_report_missing.html', {'missing': missing})



def view_missing_report(request, case_id):
    report = CaseReport.objects.filter(missing_person_id=case_id).first()
    return render(request, 'police/view_missing_report.html', {'report': report})


def user_view_missing_reports(request):
    user = User.objects.get(user=request.user)
    reports = CaseReport.objects.filter(missing_person__user=user)
    return render(request, 'user/view_missing_reports.html', {'reports': reports})


######################## Crime Case  ########################


def report_crime(request):
    login_user = Login.objects.get(id=request.user.id)
    user = User.objects.get(user=login_user)
    departments = Police_department.objects.all()

    if request.method == 'POST':
        crime_type = request.POST['crime_type']
        location = request.POST['location']
        description = request.POST['description']
        department_id = request.POST['department']
        department = Police_department.objects.get(id=department_id)
        evidence = request.FILES.get('evidence')

        CrimeReport.objects.create(
            user=user,
            department=department,
            crime_type=crime_type,
            location=location,
            description=description,
            evidence=evidence
        )
        return redirect('my_crime_reports')  # Redirect to user's crime report list page

    return render(request, 'user/report_crime.html', {'departments': departments})



def my_crime_reports(request):
    login_user = Login.objects.get(id=request.user.id)
    user = User.objects.get(user=login_user)
    reports = CrimeReport.objects.filter(user=user)
    return render(request, 'user/my_crime_reports.html', {'reports': reports})


def police_crime_reports(request):
    police = Police_department.objects.get(user=request.user)
    reports = CrimeReport.objects.filter(department=police)
    return render(request, 'police/police_crime_reports.html', {'reports': reports})



def update_crime_status(request, report_id):
    if request.method == 'POST':
        new_status = request.POST['status']
        crime_report = get_object_or_404(CrimeReport, id=report_id)
        crime_report.status = new_status
        crime_report.save()
        messages.success(request, 'Crime report status updated successfully.')
    return redirect('police_crime_reports')


def add_case_report_crime(request, crime_id):
    police = Police_department.objects.get(user=request.user)
    crime = get_object_or_404(CrimeReport, id=crime_id)

    if request.method == 'POST':
        case_evidence = request.POST['case_evidence']
        description = request.POST['description']
        report_file = request.FILES.get('report_file')

        CaseReport.objects.create(
            crime_report=crime,
            police=police,
            case_evidence=case_evidence,
            description=description,
            report_file=report_file
        )

        crime.status = 'Resolved'
        crime.save()
        messages.success(request, 'Crime report successfully submitted.')
        return redirect('police_crime_reports')

    return render(request, 'police/add_case_report_crime.html', {'crime': crime})



def view_crime_report(request, case_id):
    report = CaseReport.objects.filter(crime_report_id=case_id).first()
    return render(request, 'police/view_crime_report.html', {'report': report})


def user_view_crime_reports(request):
    user = User.objects.get(user=request.user)
    reports = CaseReport.objects.filter(crime_report__user=user)
    return render(request, 'user/user_view_crime_reports.html', {'reports': reports})


#################################### Missing search ##################

def search_missing_person(request):
    user = User.objects.get(user=request.user)
    missing_persons = None
    pincode = ''

    if request.method == 'POST':
        pincode = request.POST.get('pincode')
        missing_persons = MissingPerson.objects.filter(user=user, pincode=pincode)

    return render(request, 'user/search_missing_person.html', {
        'missing_persons': missing_persons,
        'pincode': pincode
    })


def view_missing_report_search(request, case_id):
    report = CaseReport.objects.filter(missing_person_id=case_id).first()
    return render(request, 'user/view_missing_report_search.html', {'report': report})

##################################### Complaint Search #############################

def search_complaints(request):
    user = User.objects.get(user=request.user)
    complaints = None
    title = ''
    department = ''
    status = ''

    if request.method == 'POST':
        title = request.POST.get('title')
        department = request.POST.get('department')
        status = request.POST.get('status')

        complaints = Complaint.objects.filter(user=user)

        if title:
            complaints = complaints.filter(title__icontains=title)
        if department:
            complaints = complaints.filter(department__name__icontains=department)
        if status:
            complaints = complaints.filter(status__icontains=status)

    return render(request, 'user/search_complaints.html', {
        'complaints': complaints,
        'title': title,
        'department': department,
        'status': status
    })


def view_complaint_report_search(request, complaint_id):
    report = CaseReport.objects.filter(complaint_id=complaint_id).first()
    return render(request, 'user/view_complaint_report_search.html', {'report': report})




def search_crimereports(request):
    user = User.objects.get(user=request.user)
    crimereports = None
    department = ''
    crime_type = ''
    status = ''

    if request.method == 'POST':
        department = request.POST.get('department')
        crime_type = request.POST.get('crime_type')
        status = request.POST.get('status')

        crimereports = CrimeReport.objects.filter(user=user)

        if department:
            crimereports = crimereports.filter(department__name__icontains=department)
        if crime_type:
            crimereports = crimereports.filter(crime_type__icontains=crime_type)
        if status:
            crimereports = crimereports.filter(status__icontains=status)

    return render(request, 'user/search_crimereports.html', {
        'crimereports': crimereports,
        'department': department,
        'crime_type': crime_type,
        'status': status
    })


def view_crime_report_search(request, crime_id):
    report = CaseReport.objects.filter(crime_report_id=crime_id).first()
    return render(request, 'user/view_crime_report_search.html', {'report': report})



# views.py
from django.db.models import Q


def view_all_reports(request):
    user = User.objects.get(user=request.user)

    complaints = Complaint.objects.filter(user=user)
    missing_persons = MissingPerson.objects.filter(user=user)
    crime_reports = CrimeReport.objects.filter(user=user)

    complaint_search = request.GET.get('complaint_search', '')
    missing_search = request.GET.get('missing_search', '')
    crime_search = request.GET.get('crime_search', '')

    if complaint_search:
        complaints = complaints.filter(
            Q(title__icontains=complaint_search) |
            Q(description__icontains=complaint_search) |
            Q(status__icontains=complaint_search) |
            Q(date_submitted__icontains=complaint_search)
        )

    if missing_search:
        missing_persons = missing_persons.filter(
            Q(person_name__icontains=missing_search) |
            Q(age__icontains=missing_search) |
            Q(last_seen_location__icontains=missing_search) |
            Q(description__icontains=missing_search) |
            Q(status__icontains=missing_search) |
            Q(address__icontains=missing_search) |
            Q(pincode__icontains=missing_search) |
            Q(date_reported__icontains=missing_search)
        )

    if crime_search:
        crime_reports = crime_reports.filter(
            Q(crime_type__icontains=crime_search) |
            Q(location__icontains=crime_search) |
            Q(description__icontains=crime_search) |
            Q(status__icontains=crime_search) |
            Q(date_reported__icontains=crime_search)
        )

    return render(request, 'user/view_all_reports.html', {
        'complaints': complaints,
        'missing_persons': missing_persons,
        'crime_reports': crime_reports,
        'complaint_search': complaint_search,
        'missing_search': missing_search,
        'crime_search': crime_search,
    })

def user_profile(request):
    user_id = request.session.get('uid')
    profile = User.objects.get(user_id=user_id)
    return render(request, 'user/user_profile.html', {'profile': profile})

def police_profile(request):
    user_id = request.session.get('uid')
    profile = Police_department.objects.get(user_id=user_id)
    return render(request, 'police/police_profile.html', {'profile': profile})