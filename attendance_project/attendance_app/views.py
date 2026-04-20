from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password

def dlt(request):
    Attendance.objects.filter(id=2).delete()
    return redirect('/')

# Create your views here.
def index(request):
    return render(request, 'index.html')

def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'teacher/teacher_dashboard.html')

def student_dashboard(request):
    return render(request, 'student/student_dashboard.html')

# def admin(request):
#     adm=Login.objects.create_superuser(username='admin',email='admin@gmail.com',viewpassword='1234',password='1234',usertype='Admin')
#     adm.save()
#     return redirect('/')


def logins(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # ADMIN login (hardcoded)
        if username == "admin" and password == "1234":
            request.session['username'] = username
            request.session['usertype'] = "admin"
            return redirect('/admin_dashboard')

        # Check in Login table
        user = Login.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            # Store session
            request.session['username'] = user.username
            request.session['usertype'] = user.usertype
            request.session['user_id'] = user.id

            if user.usertype == "student":
                return redirect('/student_dashboard/')
            elif user.usertype == "teacher":
                if user.is_active:
                    return redirect('/teacher_dashboard/')
                else:
                    return render(request, "login.html", {"error": "Your account is not active. Please wait for admin approval."})
            else:
                return render(request, "login.html", {"error": "Invalid user type."})
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, 'login.html')


import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from .models import Login, Student

def student_register(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        batch = request.POST.get('batch', '')
        year = request.POST.get('year', '')
        profile_picture = request.FILES.get('profile_picture')

        # Auto-generate password same as email
        password = make_password(email)

        # Create Login entry
        login_user = Login.objects.create(
            username=username,
            email=email,
            password=password,
            viewpassword=email,
            usertype="student",
            is_active=True
        )

        # Generate OTP
        otp_code = ''.join(random.choices(string.digits, k=6))

        # Create Student entry
        Student.objects.create(
            user=login_user,
            fullname=fullname,
            phone=phone,
            address=address,
            email=email,
            batch=batch,
            year=year,
            profile_picture=profile_picture,
            otp=otp_code,
            is_verified=False
        )

        # Send OTP email
        send_mail(
            subject="Verify your email",
            message=f"Your OTP code is {otp_code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        request.session['email'] = email
        return redirect('verify_otp')

    return render(request, "student_register.html")



def verify_otp(request):
    email = request.session.get('email')
    if not email:
        return redirect('student_register')

    if request.method == "POST":
        entered_otp = request.POST['otp']
        student = Student.objects.filter(email=email, otp=entered_otp).first()

        if student:
            student.is_verified = True
            # student.otp = None

            # Generate random password
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            student.user.password = make_password(new_password)
            student.user.viewpassword = new_password
            student.user.save()
            student.save()

            # Send generated password
            send_mail(
                subject="Your account password",
                message=f"Your account is verified. Your login password is: {new_password}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            )

            return redirect('logins')
        else:
            return render(request, "otp.html", {"error": "Invalid OTP"})

    return render(request, "otp.html")


def teacher_register(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        batch = request.POST.get('batch', '')
        profile_picture = request.FILES.get('profile_picture')

        # Generate random password
        generated_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Create Login entry with is_active=False
        login_user = Login.objects.create(
            username=username,
            email=email,
            password=make_password(generated_password),
            viewpassword=generated_password,
            usertype="teacher",
            is_active=False
        )

        # Create Teacher profile
        Teacher.objects.create(
            user=login_user,
            fullname=fullname,
            phone=phone,
            address=address,
            email=email,
            batch=batch,
            profile_picture=profile_picture
        )

        # Send credentials email
        send_mail(
            subject="Your Teacher Account Details",
            message=f"Hello {fullname},\n\nYour account has been created.\nUsername: {username}\nPassword: {generated_password}\n\nYour account is pending admin approval.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        return render(request, "login.html", {"email": email})

    return render(request, "teacher_register.html")


def display_students(request):
    students = Student.objects.all().select_related('user')
    return render(request, 'admin/display_students.html', {'students': students})

def display_teachers(request):
    teachers = Teacher.objects.all().select_related('user')
    return render(request, 'admin/display_teachers.html', {'teachers': teachers})

def approve_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.user.is_active = True
    teacher.user.save()
    return redirect('display_teachers')

def reject_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.user.is_active = False
    teacher.user.save()
    return redirect('display_teachers')

def student_profile(request):
    # Check if the session has a logged-in user
    if 'user_id' not in request.session or request.session.get('usertype') != 'student':
        return redirect('/logins/')  # redirect to login if not logged in as student
    
    try:
        student = Student.objects.select_related('user').get(user_id=request.session['user_id'])
    except Student.DoesNotExist:
        return render(request, 'student/student_profile.html', {'error': 'Student profile not found.'})
    
    return render(request, 'student/student_profile.html', {'student': student})


def teacher_profile(request):
    # Check if the session has a logged-in teacher
    if 'user_id' not in request.session or request.session.get('usertype') != 'teacher':
        return redirect('/logins/')  # redirect to login if not logged in as teacher
    
    try:
        teacher = Teacher.objects.select_related('user').get(user_id=request.session['user_id'])
    except Teacher.DoesNotExist:
        return render(request, 'teacher/teacher_profile.html', {'error': 'Teacher profile not found.'})
    
    return render(request, 'teacher/teacher_profile.html', {'teacher': teacher})


def assign_teacher(request):
    teachers = Teacher.objects.all()
    selected_teacher = None
    students = []
    student_years = []

    if request.method == "GET" and "teacher_id" in request.GET:
        teacher_id = request.GET.get("teacher_id")
        selected_teacher = get_object_or_404(Teacher, id=teacher_id)

        # Filter students by teacher's batch
        students = Student.objects.filter(batch=selected_teacher.batch)
        student_years = students.values_list("year", flat=True).distinct()

    if request.method == "POST":
        teacher_id = request.POST.get("teacher_id")
        year = request.POST.get("year")
        selected_teacher = get_object_or_404(Teacher, id=teacher_id)

        # Assign teacher to students of same batch & year
        Student.objects.filter(batch=selected_teacher.batch, year=year).update(assigned_teacher=selected_teacher)

        return redirect("assign_teacher")  # Replace with your URL name

    return render(request, "admin/assign_teacher.html", {
        "teachers": teachers,
        "selected_teacher": selected_teacher,
        "students": students,
        "student_years": student_years,
    })

def display_assigned_teachers(request):
    teachers = Teacher.objects.prefetch_related('students').all()
    return render(request, "admin/display_assigned_teachers.html", {"teachers": teachers})


from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from datetime import datetime
from django.utils import timezone

def mark_attendance(request):
    if request.session.get("usertype") != "teacher":
        return render(request, "error.html", {"message": "Unauthorized access."})

    try:
        teacher = Teacher.objects.get(user_id=request.session["user_id"])
    except Teacher.DoesNotExist:
        return render(request, "error.html", {"message": "Teacher profile not found."})

    students = Student.objects.filter(assigned_teacher=teacher)

    if request.method == "POST":
        # Get date from form (or fallback to today if missing)
        selected_date_str = request.POST.get("date")
        if selected_date_str:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        else:
            selected_date = timezone.now().date()

        time_slot = request.POST.get("time_slot", "10-11")

        # ✅ Check if attendance already exists for this teacher/date/time_slot
        already_exists = Attendance.objects.filter(
            teacher=teacher,
            date=selected_date,
            time_slot=time_slot
        ).exists()

        if already_exists:
            messages.error(request, f"Attendance for {selected_date} ({time_slot}) is already saved.")
            return redirect("mark_attendance")

        # ✅ Save attendance only if not already present
        for student in students:
            status = request.POST.get(f"status_{student.id}", "Absent")
            Attendance.objects.create(
                student=student,
                teacher=teacher,
                date=selected_date,
                time_slot=time_slot,
                status=status
            )

        messages.success(request, f"Attendance saved for {selected_date} ({time_slot}).")
        return redirect("mark_attendance")

    return render(
        request,
        "teacher/mark_attendance.html",
        {
            "students": students,
            "teacher": teacher,
            "today": timezone.now().date(),
        }
    )


def manage_attendance(request):
    if request.session.get("usertype") != "teacher":
        return render(request, "error.html", {"message": "Unauthorized access."})

    try:
        teacher = Teacher.objects.get(user_id=request.session["user_id"])
    except Teacher.DoesNotExist:
        return render(request, "error.html", {"message": "Teacher profile not found."})

    # Defaults
    selected_date_str = request.GET.get("date") or timezone.now().date().strftime("%Y-%m-%d")
    selected_time_slot = request.GET.get("time_slot", "10-11")

    if request.method == "POST":
        selected_date_str = request.POST.get("date")
        selected_time_slot = request.POST.get("time_slot", "10-11")

    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()

    # Fetch or create attendance records for this date + time slot
    students = Student.objects.filter(assigned_teacher=teacher)
    attendance_records = []
    for student in students:
        record, _ = Attendance.objects.get_or_create(
            student=student,
            teacher=teacher,
            date=selected_date,
            time_slot=selected_time_slot,
            defaults={"status": "Absent"}
        )
        attendance_records.append(record)

    if request.method == "POST":
        for record in attendance_records:
            status = request.POST.get(f"status_{record.student.id}", "Absent")
            record.status = status
            record.time_slot = selected_time_slot  # ✅ fix applied
            record.save()

        return redirect(f"/manage_attendance/?date={selected_date}&time_slot={selected_time_slot}")

    return render(request, "teacher/manage_attendance.html", {
        "teacher": teacher,
        "selected_date": selected_date,
        "selected_time_slot": selected_time_slot,
        "attendance_records": attendance_records
    })


def attendance_percentage(request):
    if request.session.get("usertype") != "teacher":
        return render(request, "error.html", {"message": "Unauthorized access."})

    try:
        teacher = Teacher.objects.get(user_id=request.session["user_id"])
    except Teacher.DoesNotExist:
        return render(request, "error.html", {"message": "Teacher profile not found."})

    students = Student.objects.filter(assigned_teacher=teacher)

    student_data = []
    for student in students:
        total_classes = Attendance.objects.filter(student=student).count()
        present_classes = Attendance.objects.filter(student=student, status="Present").count()
        
        percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0

        student_data.append({
            "student": student,
            "total": total_classes,
            "present": present_classes,
            "percentage": round(percentage, 2),
        })

    return render(request, "teacher/attendance_percentage.html", {
        "teacher": teacher,
        "student_data": student_data,
    })


def student_attendance(request):
    if request.session.get("usertype") != "student":
        return render(request, "error.html", {"message": "Unauthorized access."})

    try:
        student = Student.objects.get(user_id=request.session["user_id"])
    except Student.DoesNotExist:
        return render(request, "error.html", {"message": "Student profile not found."})

    # Fetch all attendance records for this student
    attendance_records = Attendance.objects.filter(student=student).order_by("-date")

    total_classes = attendance_records.count()
    present_classes = attendance_records.filter(status="Present").count()
    percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0

    return render(request, "student/student_attendance.html", {
        "student": student,
        "attendance_records": attendance_records,
        "total_classes": total_classes,
        "present_classes": present_classes,
        "percentage": round(percentage, 2),
    })