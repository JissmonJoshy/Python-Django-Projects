from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import *
import re
from django.contrib.auth.hashers import check_password


# Create your views here.
def index(request):
    return render(request, 'index.html')

def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def user_dashboard(request):
    return render(request, 'user/user_dashboard.html')

def employee_dashboard(request):
    return render(request, 'employee/employee_dashboard.html')
def adm(request):
    adm=Login.objects.create_superuser(username='admin',email='admin@gmail.com',viewpassword='admin',password='1234',usertype='admin')
    adm.save()
    return redirect('/')

def user_register(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        image = request.FILES.get('profile_image')

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('user_register')

        if Login.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('user_register')

        if not (email.endswith('@gmail.com') or email.endswith('@gmail.in')):
            messages.error(request, "Only Gmail (.com or .in) is allowed")
            return redirect('user_register')

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be exactly 10 digits")
            return redirect('user_register')

        login_obj = Login.objects.create(
            username=username,
            email=email,
            usertype='user',
            viewpassword=password,
            password=make_password(password)
        )

        User.objects.create(
            login=login_obj,
            full_name=full_name,
            address=address,
            mobile=phone,
            email=email,
            profile_image=image
        )

        messages.success(request, "Registration successful")
        return redirect('user_register')

    return render(request, 'user_register.html')


def employee_register(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        operation = request.POST.get('operation')  # simple text
        image = request.FILES.get('profile_image')

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('employee_register')

        if Login.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('employee_register')

        if not (email.endswith('@gmail.com') or email.endswith('@gmail.in')):
            messages.error(request, "Only Gmail (.com or .in) is allowed")
            return redirect('employee_register')

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Mobile number must be exactly 10 digits")
            return redirect('employee_register')

        if not operation:
            messages.error(request, "Please select workshop operation")
            return redirect('employee_register')

        login_obj = Login.objects.create(
            username=username,
            email=email,
            usertype='employee',
            viewpassword=password,
            password=make_password(password),
            is_active=False
        )

        Employee.objects.create(
            login=login_obj,
            full_name=full_name,
            address=address,
            mobile=phone,
            email=email,
            operation=operation,  # save selected text
            profile_image=image
        )

        messages.success(request, "Employee registered successfully! Wait for admin approval.")
        return redirect('employee_register')

    return render(request, 'employee_register.html')




def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # ADMIN LOGIN (STATIC)
        if username == "admin" and password == "admin":
            request.session['login_id'] = "admin"
            request.session['usertype'] = "admin"
            messages.success(request, "Admin login successful")
            return redirect('admin_dashboard')
        

        try:
            user = Login.objects.get(username=username)

            if check_password(password, user.password):
                request.session['login_id'] = user.id
                request.session['usertype'] = user.usertype

                if user.usertype == "user":
                    messages.success(request, "User login successful")
                    return redirect('user_dashboard')

                elif user.usertype == "employee":
                    messages.success(request, "Employee login successful")
                    return redirect('employee_dashboard')

                else:
                    messages.error(request, "Invalid user role")
            else:
                messages.error(request, "Invalid password")

        except Login.DoesNotExist:
            messages.error(request, "Invalid username")

    return render(request, 'login.html')


def view_users(request):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    users = User.objects.all()
    return render(request, 'admin/view_users.html', {'users': users})


def view_employees(request):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    employees = Employee.objects.all()
    return render(request, 'admin/view_employees.html', {'employees': employees})


def approve_employee(request, login_id):
    login = Login.objects.get(id=login_id)
    login.is_active = True
    login.save()
    messages.success(request, "Employee approved successfully")

    return redirect('view_employees')


def reject_employee(request, login_id):
    Employee.objects.filter(login_id=login_id).delete()
    Login.objects.filter(id=login_id).delete()
    messages.success(request, "Employee rejected and deleted successfully")

    return redirect('view_employees')


def user_profile(request):
    if request.session.get('usertype') != 'user':
        return redirect('login')

    user_id = request.session.get('login_id')
    user = User.objects.get(login_id=user_id)
    return render(request, 'user/user_profile.html', {'user': user})


# User profile edit
def user_profile_edit(request):
    if request.session.get('usertype') != 'user':
        return redirect('login')

    user_id = request.session.get('login_id')
    user = User.objects.get(login_id=user_id)

    if request.method == "POST":
        user.full_name = request.POST.get('full_name')
        user.address = request.POST.get('address')
        user.mobile = request.POST.get('mobile')
        user.email = request.POST.get('email')

        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES.get('profile_image')

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('user_profile')

    return render(request, 'user/user_profile_edit.html', {'user': user})


# Employee profile view
def employee_profile(request):
    if request.session.get('usertype') != 'employee':
        return redirect('login')

    employee_id = request.session.get('login_id')
    employee = Employee.objects.get(login_id=employee_id)
    return render(request, 'employee/employee_profile.html', {'employee': employee})


# Employee profile edit
def employee_profile_edit(request):
    if request.session.get('usertype') != 'employee':
        return redirect('login')

    employee_id = request.session.get('login_id')
    employee = Employee.objects.get(login_id=employee_id)

    if request.method == "POST":
        employee.full_name = request.POST.get('full_name')
        employee.address = request.POST.get('address')
        employee.mobile = request.POST.get('mobile')
        employee.email = request.POST.get('email')
        employee.operation = request.POST.get('operation')

        if request.FILES.get('profile_image'):
            employee.profile_image = request.FILES.get('profile_image')

        employee.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('employee_profile')

    return render(request, 'employee/employee_profile_edit.html', {'employee': employee})

def add_services(request):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    if request.method == "POST":
        service_name = request.POST.get('service_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        operation = request.POST.get('operation')
        image = request.FILES.get('image')

        Service.objects.create(
            service_name=service_name,
            description=description,
            price=price,
            operation=operation,
            image=image
        )

        messages.success(request, "Service added successfully")
        return redirect('add_services')

    return render(request, 'admin/add_services.html')



def view_services(request):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    services = Service.objects.all()
    return render(request, 'admin/view_services.html', {'services': services})


def edit_services(request, service_id):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    service = Service.objects.get(id=service_id)

    if request.method == "POST":
        service.service_name = request.POST.get('service_name')
        service.description = request.POST.get('description')
        service.price = request.POST.get('price')
        service.operation = request.POST.get('operation')

        if request.FILES.get('image'):
            service.image = request.FILES.get('image')

        service.save()
        messages.success(request, "Service updated successfully")
        return redirect('view_services')

    return render(request, 'admin/edit_services.html', {'service': service})



def delete_services(request, service_id):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    service = Service.objects.get(id=service_id)
    service.delete()
    messages.success(request, "Service deleted successfully")
    return redirect('view_services')



def user_view_services(request):
    if request.session.get('usertype') != 'user':
        return redirect('login')

    services = Service.objects.all()
    return render(request, 'user/user_view_services.html', {'services': services})


def book_service(request, service_id):
    if request.session.get('usertype') != 'user':
        return redirect('login')

    user_id = request.session.get('login_id')
    user = User.objects.get(login_id=user_id)
    service = Service.objects.get(id=service_id)

    if request.method == "POST":
        car_number = request.POST.get('car_number')
        car_name = request.POST.get('car_name')
        description = request.POST.get('description')
        image = request.FILES.get('car_image')

        ServiceBooking.objects.create(
            user=user,
            service=service,
            car_number=car_number,
            car_name=car_name,
            problem_description=description,
            car_image=image,
            status='Pending'
        )

        messages.success(request, "Service booked successfully! Status: Pending")
        return redirect('user_view_services')

    return render(request, 'user/book_service.html', {'service': service})

def my_bookings(request):
    if request.session.get('usertype') != 'user':
        return redirect('login')

    user_id = request.session.get('login_id')
    user = User.objects.get(login_id=user_id)

    bookings = ServiceBooking.objects.filter(user=user).order_by('-booking_date')

    return render(request, 'user/my_bookings.html', {
        'bookings': bookings
    })


def all_bookings(request):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    bookings = ServiceBooking.objects.all().order_by('-booking_date')
    return render(request, 'admin/all_bookings.html', {'bookings': bookings})

def update_booking_status(request, booking_id, status):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    booking = ServiceBooking.objects.get(id=booking_id)
    booking.status = status
    booking.save()

    messages.success(request, f"Booking {status} successfully")
    return redirect('all_bookings')


def assign_booking(request, booking_id):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    booking = ServiceBooking.objects.get(id=booking_id)

    employees = Employee.objects.filter(
        operation=booking.service.operation,
        login__is_active=True
    )

    if request.method == "POST":
        employee_id = request.POST.get('employee')
        employee = Employee.objects.get(id=employee_id)

        booking.employee = employee
        booking.status = "Assigned"
        booking.save()

        messages.success(request, "Booking assigned to employee successfully")
        return redirect('all_bookings')

    return render(request, 'admin/assign_booking.html', {
        'booking': booking,
        'employees': employees
    })

def make_payment(request, booking_id):
    if request.session.get('usertype') != 'user':
        return redirect('login')

    booking = ServiceBooking.objects.get(id=booking_id)

    if request.method == "POST":
        booking.status = "Paid"
        booking.save()
        messages.success(request, "Payment successful")
        return redirect('my_bookings')

    return render(request, 'user/payment.html', {
        'booking': booking
    })




def assigned_works(request):
    if request.session.get('usertype') != 'employee':
        return redirect('login')

    login_id = request.session.get('login_id')

    employee = Employee.objects.get(login_id=login_id)

    works = ServiceBooking.objects.filter(employee=employee)

    return render(request, 'employee/assigned_works.html', {
        'works': works
    })

def add_parts(request):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    if request.method == "POST":
        Part.objects.create(
            part_name=request.POST.get('part_name'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            stock=request.POST.get('stock'),
            operation=request.POST.get('operation'),
            image=request.FILES.get('image')
        )
        messages.success(request, "Part added successfully")
        return redirect('add_parts')

    return render(request, 'admin/add_parts.html')

def view_parts(request):
    parts = Part.objects.all()
    return render(request, 'admin/view_parts.html', {'parts': parts})


def edit_part(request, part_id):
    part = Part.objects.get(id=part_id)

    if request.method == "POST":
        part.part_name = request.POST.get('part_name')
        part.description = request.POST.get('description')
        part.price = request.POST.get('price')
        part.stock = request.POST.get('stock')
        part.operation = request.POST.get('operation')

        if request.FILES.get('image'):
            part.image = request.FILES.get('image')

        part.save()
        return redirect('view_parts')

    return render(request, 'admin/edit_parts.html', {'part': part})


def delete_part(request, part_id):
    Part.objects.get(id=part_id).delete()
    return redirect('view_parts')

def user_view_parts(request):
    if request.session.get('usertype') != 'user':
        return redirect('login')

    parts = Part.objects.all()
    return render(request, 'user/user_view_parts.html', {'parts': parts})

def book_part(request, part_id):
    if request.session.get('usertype') != 'user':
        return redirect('login')

    user_id = request.session.get('login_id')
    user = User.objects.get(login_id=user_id)
    part = Part.objects.get(id=part_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))

        if quantity > part.stock:
            messages.error(request, "Requested quantity not available")
            return redirect('book_part', part_id=part.id)

        PartBooking.objects.create(
            user=user,
            part=part,
            quantity=quantity
        )

        messages.success(request, "Part booked successfully")
        return redirect('my_part_bookings')

    return render(request, 'user/book_part.html', {'part': part})

def my_part_bookings(request):
    if request.session.get('usertype') != 'user':
        return redirect('login')

    user_id = request.session.get('login_id')
    user = User.objects.get(login_id=user_id)

    bookings = PartBooking.objects.filter(user=user)
    return render(request, 'user/my_part_bookings.html', {'bookings': bookings})


def delete_part_booking(request, booking_id):
    if request.session.get('usertype') != 'user':
        return redirect('login')

    booking = PartBooking.objects.get(id=booking_id)
    if booking.user.login.id == request.session.get('login_id'):
        booking.delete()
        messages.success(request, "Booking deleted successfully!")
    else:
        messages.error(request, "You cannot delete this booking.")
    return redirect('my_part_bookings')


def part_payment(request, id):
    booking = get_object_or_404(PartBooking, id=id)

    if request.method == "POST":
        booking.status = "Paid"
        stock_after_booking = booking.part.stock - booking.quantity
        booking.part.stock = stock_after_booking
        booking.part.save()

        booking.save()
        messages.success(request, "Payment successful")
        return redirect('my_part_bookings')

    return render(request, 'user/parts_payment.html', {'booking': booking})


def delete_service_booking(request, id):
    booking = get_object_or_404(ServiceBooking, id=id)
    booking.delete()
    return redirect('my_bookings')


def all_parts_bookings(request):
    bookings = PartBooking.objects.all().order_by('-booked_date')
    return render(request, 'admin/all_parts_bookings.html', {'bookings': bookings})

def mark_part_delivered(request, id):
    booking = get_object_or_404(PartBooking, id=id)
    booking.status = "Delivered"
    booking.save()
    return redirect('all_parts_bookings')


def update_work_progress(request, id):
    work = ServiceBooking.objects.get(id=id)

    if request.method == "POST":
        work.estimate_date = request.POST.get('estimate_date')
        work.progress = int(request.POST.get('progress'))

        if work.progress == 100:
            work.status = 'Completed'
        else:
            work.status = 'In Progress'

        work.save()

    return redirect('assigned_works')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee, Part, EmployeePartBooking

def view_employee_parts(request):
    if request.session.get('usertype') != 'employee':
        return redirect('login')

    login_id = request.session.get('login_id')
    employee = Employee.objects.get(login_id=login_id)
    parts = Part.objects.all()

    return render(request, 'employee/view_employee_parts.html', {
        'parts': parts,
        'employee': employee
    })


def book_employee_part(request, part_id):
    if request.session.get('usertype') != 'employee':
        return redirect('login')

    login_id = request.session.get('login_id')
    employee = Employee.objects.get(login_id=login_id)
    part = get_object_or_404(Part, id=part_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))
        if quantity > part.stock:
            messages.error(request, f"Only {part.stock} items in stock!")
            return redirect('view_employee_parts')

        # Create booking with status 'Pending'
        EmployeePartBooking.objects.create(
            employee=employee,
            part=part,
            quantity=quantity,
            status='Pending'
        )

        # Reduce stock
        part.stock -= quantity
        part.save()

        messages.success(request, f"{part.part_name} booked successfully!")
        return redirect('employee_part_bookings')

    return render(request, 'employee/book_employee_part.html', {
        'part': part
    })


def employee_part_bookings(request):
    if request.session.get('usertype') != 'employee':
        return redirect('login')

    login_id = request.session.get('login_id')
    employee = Employee.objects.get(login_id=login_id)
    bookings = EmployeePartBooking.objects.filter(employee=employee).order_by('-booked_date')

    return render(request, 'employee/employee_part_bookings.html', {
        'bookings': bookings
    })


def employee_payment(request, booking_id):
    if request.session.get('usertype') != 'employee':
        return redirect('login')

    login_id = request.session.get('login_id')
    employee = Employee.objects.get(login_id=login_id)
    booking = get_object_or_404(EmployeePartBooking, id=booking_id, employee=employee)

    if request.method == "POST":
        # Here, you can integrate actual payment gateway if needed
        # For now, we just update status to Paid
        booking.status = 'Paid'
        booking.save()
        messages.success(request, f"{booking.part.part_name} payment successful!")
        return redirect('employee_part_bookings')

    return render(request, 'employee/employee_payment.html', {
        'booking': booking
    })



def admin_view_employee_part_bookings(request):
    # Make sure user is admin
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    bookings = EmployeePartBooking.objects.all().order_by('-booked_date')

    return render(request, 'admin/employee_parts_bookings.html', {
        'bookings': bookings
    })


def admin_mark_employee_part_delivered(request, booking_id):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    booking = get_object_or_404(EmployeePartBooking, id=booking_id)
    if booking.status == 'Paid':
        booking.status = 'Delivered'
        booking.save()
        messages.success(request, f"{booking.part.part_name} marked as Delivered!")
    return redirect('admin_view_employee_part_bookings')
