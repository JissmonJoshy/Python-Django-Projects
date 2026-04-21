from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout
from datetime import date as date
from django.db.models import Q, Min, Max
from datetime import datetime, timedelta
from django.utils.timezone import now

def index(request):
    return render(request, 'index.html')

def user_logout(request):
    logout(request)
    return redirect('index')


def admin(request):
    adm=Login.objects.create_superuser(username='admin',email='admin@gmail.com',viewpassword='1234',password='1234',usertype='Admin')
    adm.save()
    return redirect('/')

def view_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']       
        
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            if user.is_active:
                auth_login(request, user)  

                if user.usertype == "Admin":
                    return redirect('admin_dashboard')

                elif user.usertype == "Patient":
                    request.session['uid'] = user.id  
                    return redirect('patient_dashboard')

                elif user.usertype == "Lab Technician":
                    request.session['uid'] = user.id
                    return redirect('lab_dashboard')

                elif user.usertype == "Dentist":
                    request.session['uid'] = user.id
                    return redirect('dentist_dashboard')

                else:
                    return redirect('login')  
            else:
                messages.error(request, 'Your account is inactive')
                return render(request, 'login.html')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')


def admin_dashboard(request):
    patient_count = Patient.objects.filter(patient_id__is_active=True).count()
    dentist_count = Dentist.objects.filter(dentist_id__is_active=True).count()
    lab_count = Lab.objects.filter(lab_id__is_active=True).count()

    return render(request, 'admin/admin_dashboard.html', {
        'patient_count': patient_count,
        'dentist_count': dentist_count,
        'lab_count': lab_count
    })

def lab_dashboard(request):
    return render(request, 'lab/lab_dashboard.html')

def patient_dashboard(request):
    return render(request, 'patient/patient_dashboard.html')

def dentist_dashboard(request):
    return render(request, 'dentist/dentist_dashboard.html')



import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Login, Patient

def patient_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        image = request.FILES.get('image')
        state = request.POST['state']
        district= request.POST['district']
        pincode = request.POST['pincode']

        # Validate email format for Gmail and domain restrictions
        email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
        domain_pattern = r'.+\.(in|com)$'

        if not re.match(email_pattern, email):
            messages.error(request, 'Only Gmail addresses are allowed.')
            return redirect('patient_register')

        if not re.match(domain_pattern, email):
            messages.error(request, 'Email must have a .in or .com domain.')
            return redirect('patient_register')

        if Login.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('patient_register')

        if Login.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('patient_register')

        if Patient.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number is already registered.')
            return redirect('patient_register')

        login_user = Login.objects.create(
            username=username,
            usertype="Patient",
            email=email,
            viewpassword=password,
            is_active=False  
        )
        login_user.set_password(password)
        login_user.save()

        patient = Patient.objects.create(
            patient_id=login_user,
            username=username,
            name=name,
            email=email,
            phone=phone,
            address=address,
            image=image,
            state=state,
            district=district,
            pincode=pincode
    
        )
        patient.save()

        messages.success(request, 'Patient registered successfully! Waiting for admin approval.')
        return redirect('view_login')  

    return render(request, 'patient_register.html')


def dentist_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        image = request.FILES.get('image')
        licence = request.FILES.get('licence')
        experience = request.FILES.get('experience')
        state = request.POST['state']
        district= request.POST['district']
        pincode = request.POST['pincode']

        email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
        domain_pattern = r'.+\.(in|com)$'

        if not re.match(email_pattern, email):
            messages.error(request, 'Only Gmail addresses are allowed.')
            return redirect('patient_register')

        if not re.match(domain_pattern, email):
            messages.error(request, 'Email must have a .in or .com domain.')
            return redirect('patient_register')

        if Login.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('dentist_register')

        if Login.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('dentist_register')

        if Dentist.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number is already registered.')
            return redirect('dentist_register')

        login_user = Login.objects.create(
            username=username,
            usertype="Dentist",
            email=email,
            viewpassword=password,
            is_active=False  
        )
        login_user.set_password(password)
        login_user.save()

        dentist = Dentist.objects.create(
            dentist_id=login_user,
            username=username,
            name=name,
            email=email,
            phone=phone,
            address=address,
            image=image,
            licence= licence,
            experience = experience,
            state = state,
            district = district,
            pincode = pincode

        )
        dentist.save()

        messages.success(request, 'Dentist registered successfully! Waiting for admin approval.')
        return redirect('view_login')  

    return render(request, 'dentist_registration.html')



def lab_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        image = request.FILES.get('image')
        state = request.POST['state']
        district= request.POST['district']
        pincode = request.POST['pincode']

        email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
        domain_pattern = r'.+\.(in|com)$'

        if not re.match(email_pattern, email):
            messages.error(request, 'Only Gmail addresses are allowed.')
            return redirect('patient_register')

        if not re.match(domain_pattern, email):
            messages.error(request, 'Email must have a .in or .com domain.')
            return redirect('patient_register')

        if Login.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('lab_register')

        if Login.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('lab_register')

        if Lab.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number is already registered.')
            return redirect('lab_register')

        login_user = Login.objects.create(
            username=username,
            usertype="Lab Technician",
            email=email,
            viewpassword=password,
            is_active=False  
        )
        login_user.set_password(password)
        login_user.save()

        lab = Lab.objects.create(
            lab_id=login_user,
            username=username,
            name=name,
            email=email,
            phone=phone,
            address=address,
            image=image,
            state=state,
            district=district,
            pincode=pincode,
        
        )
        lab.save()

        messages.success(request, 'Lab registered successfully! Waiting for admin approval.')
        return redirect('view_login')  

    return render(request, 'lab_register.html')

def display_all_dentist(request):
    dentists = Dentist.objects.all()
    return render(request, 'admin/display_all_dentist.html', {'dentists': dentists})

def display_all_patient(request):
    patients = Patient.objects.all()
    return render(request, 'admin/display_all_patient.html', {'patients': patients})


def display_all_lab(request):
    labs = Lab.objects.all()
    return render(request, 'admin/display_all_lab.html', {'labs': labs})



def approve_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    login_user = patient.patient_id  # Linked Login model
    login_user.is_active = True  
    login_user.save()
    messages.success(request, f"Patient {patient.username} has been approved!")
    return redirect('display_all_patient')

def reject_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    login_user = patient.patient_id  
    patient.delete()
    login_user.delete()
    messages.success(request, f"Patient {patient.username} has been rejected and removed!")
    return redirect('display_all_patient')

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    login_user = patient.patient_id  
    
    if login_user.is_active:  
        patient.delete()
        login_user.delete()
        messages.success(request, f"Patient {patient.username} has been deleted successfully!")
    else:
        messages.error(request, "You cannot delete a user who is not yet approved!")
    return redirect('display_all_patient')


def approve_dentist(request, dentist_id):
    dentist = get_object_or_404(Dentist, id=dentist_id)
    login_user = dentist.dentist_id  
    login_user.is_active = True  
    login_user.save()
    messages.success(request, f"Dentist {dentist.username} has been approved!")
    return redirect('display_all_dentist')

def reject_dentist(request, dentist_id):
    dentist = get_object_or_404(Dentist, id=dentist_id)
    login_user = dentist.dentist_id  
    dentist.delete()
    login_user.delete()
    messages.success(request, f"Dentist {dentist.username} has been rejected and removed!")
    return redirect('display_all_dentist')

def delete_dentist(request, dentist_id):
    dentist = get_object_or_404(Dentist, id=dentist_id)
    login_user = dentist.dentist_id  

    if login_user.is_active:  
        dentist.delete()
        login_user.delete()
        messages.success(request, f"Dentist {dentist.username} has been deleted successfully!")
    else:
        messages.error(request, "You cannot delete a dentist who is not yet approved!")
    return redirect('display_all_dentist')


def approve_lab(request, lab_id):
    lab = get_object_or_404(Lab, id=lab_id)
    login_user = lab.lab_id  
    login_user.is_active = True  
    login_user.save()
    messages.success(request, f"Lab {lab.username} has been approved!")
    return redirect('display_all_lab')

def reject_lab(request, lab_id):
    lab = get_object_or_404(Lab, id=lab_id)
    login_user = lab.lab_id  
    lab.delete()
    login_user.delete()
    messages.success(request, f"Lab {lab.username} has been rejected and removed!")
    return redirect('display_all_lab')

def delete_lab(request, lab_id):
    lab = get_object_or_404(Lab, id=lab_id)
    login_user = lab.lab_id  

    if login_user.is_active:  
        lab.delete()
        login_user.delete()
        messages.success(request, f"Lab {lab.username} has been deleted successfully!")
    else:
        messages.error(request, "You cannot delete a lab that is not yet approved!")

    return redirect('display_all_lab')




def add_schedule(request):
    if request.method == 'POST':
        dentist_id = request.POST['dentist']
        date = request.POST['date']  
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        price = request.POST['price']  

        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        day = date_obj.strftime("%A")  

        dentist = Dentist.objects.get(id=dentist_id)
        TimeSchedule.objects.create(
            dentist=dentist,
            day=day,  
            date=date_obj,
            start_time=start_time,
            end_time=end_time,
            price=price  
        )

        return redirect('add_schedule')  

    dentists = Dentist.objects.all()
    return render(request, 'admin/add_schedule.html', {'dentists': dentists})


def display_all_schedule(request):
    schedules = TimeSchedule.objects.all()
    return render(request,'admin/display_all_schedule.html',{'schedules':schedules})

def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(TimeSchedule, id=schedule_id)
    schedule.delete()
    return redirect('display_all_schedule')

def edit_schedule(request, schedule_id):
    schedule = get_object_or_404(TimeSchedule, id=schedule_id)
    
    if request.method == "POST":
        schedule.dentist_id = request.POST.get("dentist")
        schedule.day = request.POST.get("day")
        schedule.start_time = request.POST.get("start_time")
        schedule.end_time = request.POST.get("end_time")
        schedule.price = request.POST.get("price")  
        schedule.save()
        return redirect('display_all_schedule')  

    dentists = Dentist.objects.all()
    return render(request, 'admin/edit_schedule.html', {'schedule': schedule, 'dentists': dentists})


def display_all_dentist_schedule(request):
    if not request.user.is_authenticated:
        return redirect('login') 

    patient = Patient.objects.get(patient_id=request.user)  
    schedules = TimeSchedule.objects.all()

    
    query = request.GET.get('query', '')
    schedule_date = request.GET.get('schedule_date', '')
    day = request.GET.get('day', '')

    if query:
        schedules = schedules.filter(Q(dentist__name__icontains=query))
    if schedule_date:
        schedules = schedules.filter(date=schedule_date)
    if day:
        schedules = schedules.filter(day__icontains=day)

    appointments = Appointment.objects.filter(patient=patient)

    booked_schedules = appointments.values_list('schedule_id', flat=True)

    return render(request, 'patient/display_all_dentist_schedule.html', {
        'schedules': schedules,
        'booked_schedules': booked_schedules,
        'appointments': appointments,  
        'query': query,
        'schedule_date': schedule_date,
        'day': day
    })

def book_appointments(request, schedule_id):
    patient = Patient.objects.get(patient_id=request.user)  
    schedule = TimeSchedule.objects.get(id=schedule_id)

    if not Appointment.objects.filter(patient=patient, schedule=schedule).exists():
        Appointment.objects.create(
            patient=patient,
            dentist=schedule.dentist,
            schedule=schedule,
            status='Pending'
        )
    return redirect('display_all_dentist_schedule')





def dentist_appointments(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    try:
        dentist = Dentist.objects.get(dentist_id=request.user)  
    except Dentist.DoesNotExist:
        return redirect('login')  
    appointments = Appointment.objects.filter(dentist=dentist).select_related('patient', 'schedule')
    return render(request, 'dentist/appointments.html', {'appointments': appointments})



def patient_bookings(request):
    patient = Patient.objects.get(patient_id=request.user)  
    appointments = Appointment.objects.filter(patient=patient)  
    return render(request, 'patient/bookings.html', {'appointments': appointments})

def cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if appointment.status == "Pending":
        appointment.delete()
        messages.success(request, "Appointment canceled successfully.")
    return redirect('patient_bookings')


def confirm_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")

        if payment_method in ["Credit Card", "UPI"]:
            appointment.status = "Paid"
            appointment.save()
            messages.success(request, "Payment successful!")
            return redirect("patient_bookings")  
    return render(request, "patient/payment.html", {"appointment": appointment})


def update_appointment_status(request, appointment_id):
    if request.method == "POST":
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.status = request.POST['status']
        appointment.save()
    return redirect('dentist_appointments')





def dentist_calendar(request):
    if request.user.usertype != 'Dentist':
        return redirect('view_login')  

    try:
        dentist = Dentist.objects.get(dentist_id=request.user)
    except Dentist.DoesNotExist:
        return redirect('view_login')

    selected_date = request.GET.get('date')
    confirmed_appointments = []

    if selected_date:
        confirmed_appointments = Appointment.objects.filter(
            dentist=dentist,
            schedule__date=selected_date,
            status='Scheduled'
        ).select_related('patient', 'schedule')  

    return render(request, 'dentist/calendar.html', {
        'confirmed_appointments': confirmed_appointments,
        'selected_date': selected_date
    })


def schedule_appointment(request):
    if request.method == "POST":
        appointment_id = request.POST.get('appointment_id')
        selected_time = request.POST.get('start_time')

        try:
            appointment = Appointment.objects.get(id=appointment_id, status='Paid')
            dentist = appointment.dentist
            date = appointment.schedule.date

            # Convert selected_time to datetime format
            selected_time = datetime.strptime(selected_time, "%H:%M")
            end_time = selected_time + timedelta(minutes=15)  # End time (15 min slot)

            
            dentist_schedule = TimeSchedule.objects.filter(dentist=dentist, date=date).first()

            if not dentist_schedule:
                messages.error(request, "No available schedule for this dentist on this date.")
                return redirect('schedule_appointment')

            
            schedule_start = datetime.combine(date, dentist_schedule.start_time)
            schedule_end = datetime.combine(date, dentist_schedule.end_time)

            
            if not (schedule_start.time() <= selected_time.time() < schedule_end.time()):
                messages.error(request, "Selected time is outside the dentist's working hours.")
                return redirect('schedule_appointment')

            
            conflicting_appointments = Appointment.objects.filter(
                dentist=dentist, 
                schedule__date=date, 
                assigned_time__lt=end_time.time(), 
                assigned_time__gt=selected_time.time()
            )

            if conflicting_appointments.exists():
                messages.error(request, "Time slot is already booked. Choose another time.")
                return redirect('schedule_appointment')

            
            appointment.assigned_time = selected_time.time()
            appointment.status = 'Scheduled'  
            appointment.save()

            messages.success(request, "Appointment scheduled successfully!")
            return redirect('schedule_appointment')

        except Appointment.DoesNotExist:
            messages.error(request, "Appointment not found or not approved.")
            return redirect('schedule_appointment')

    
    approved_appointments = Appointment.objects.filter(status='Paid', assigned_time__isnull=True)

    return render(request, 'admin/schedule_appointment.html', {
        'approved_appointments': approved_appointments
    })


ORDER_PRICES = {
    "Crown": 5000,
    "Bridge": 7000,
    "Denture": 8000,
    "Braces": 15000,
    "Retainer": 3000,
    "Teeth Whitening": 4000,
    "Implant": 20000,
    "Other": 1000
}


def display_confirmed_patients(request):
    if request.user.is_authenticated:
        try:
            dentist = Dentist.objects.get(dentist_id=request.user)  
            scheduled_appointments = Appointment.objects.filter(dentist=dentist, status='Scheduled')
            labs = Lab.objects.all()  

            if request.method == "POST":
                appointment_id = request.POST.get("appointment_id")
                lab_id = request.POST.get("lab_id")
                order_type = request.POST.get("order_type")

                if appointment_id and lab_id and order_type:
                    appointment = Appointment.objects.get(id=appointment_id)
                    lab = Lab.objects.get(id=lab_id)
                    price = ORDER_PRICES.get(order_type, 0)  
                    
                    appointment.assigned_lab = lab
                    appointment.save()

                    
                    lab_order, created = LabOrder.objects.update_or_create(
                        appointment=appointment,
                        defaults={
                            "dentist": dentist,
                            "patient": appointment.patient,
                            "lab": lab,
                            "order_type": order_type,
                            "price": price
                        }
                    )

                    return redirect('display_confirmed_patients')

            return render(request, 'dentist/display_confirmed_patients.html', {
                'appointments': scheduled_appointments,  
                'labs': labs,
                'ORDER_PRICES': ORDER_PRICES
            })

        except Dentist.DoesNotExist:
            return render(request, 'dentist/display_confirmed_patients.html', {'appointments': [], 'labs': [], 'ORDER_PRICES': ORDER_PRICES})
    
    return render(request, 'dentist/display_confirmed_patients.html', {'appointments': [], 'labs': [], 'ORDER_PRICES': ORDER_PRICES})





def display_assigned_patients(request):
    try:
        lab = Lab.objects.get(lab_id=request.user)  
        assigned_patients = Appointment.objects.filter(assigned_lab=lab).prefetch_related('laborder_set')
        return render(request, 'lab/display_assigned_patients.html', {'appointments': assigned_patients})
    except Lab.DoesNotExist:
        return render(request, 'lab/display_assigned_patients.html', {'appointments': []})

def deliver_lab_order(request, order_id):
    order = get_object_or_404(LabOrder, id=order_id)

    if request.method == "POST":
        delivery_choice = request.POST.get("delivery_status")
        
        if delivery_choice in ["Delivered to Dentist", "Delivered to Patient"]:
            order.delivery_status = delivery_choice
            order.delivered_date = now()
            order.status = "Completed"
            order.save()
            return redirect("lab_orders_list")  

    return render(request, "deliver_lab_order.html", {"order": order})





def delivery_orders(request):
    lab = Lab.objects.get(lab_id=request.user)  
    orders = LabOrder.objects.filter(lab=lab)  
    return render(request, 'lab/delivery.html', {'orders': orders})


def mark_order_delivered(request, order_id):
    order = get_object_or_404(LabOrder, id=order_id)

    
    order.status = 'Completed'
    order.save()

    
    appointment = order.appointment
    appointment.status = 'Completed'
    appointment.save()

    return redirect('delivery_orders')




def assigned_lab_view(request): 
    if request.user.is_authenticated:
        appointments = Appointment.objects.filter(patient__patient_id=request.user).prefetch_related('laborder_set')
        return render(request, 'patient/assigned_lab.html', {'appointments': appointments})
    else:
        return redirect('login')


def make_payment(request, lab_order_id):
    lab_order = get_object_or_404(LabOrder, id=lab_order_id, patient__patient_id=request.user)
    
    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        
        if payment_method == "card" or payment_method == "upi":
            lab_order.status = "Paid"
            lab_order.save()
            messages.success(request, "Payment successful! Your order status has been updated.")
            return redirect("assigned_lab_view")  
        else:
            messages.error(request, "Invalid payment method selected.")
    
    return render(request, "patient/make_payment.html", {"lab_order": lab_order})



def request_order(request):
    if request.method == "POST":
        order_type = request.POST.get('order_type')
        lab = Lab.objects.get(lab_id=request.user)

        LabOrderRequest.objects.create(lab=lab, order_type=order_type)

        return redirect('lab_dashboard')  
    return render(request, 'lab/request.html')



def manage_requests(request):
    requests = LabOrderRequest.objects.all()
    return render(request, 'admin/admin_requests.html', {'requests': requests})

def update_request_status(request, request_id, action):
    lab_request = get_object_or_404(LabOrderRequest, id=request_id)
    
    if action == 'approve':
        lab_request.status = 'Approved'
    elif action == 'reject':
        lab_request.status = 'Rejected'
    
    lab_request.save()
    return redirect('manage_requests')




def lab_requests_view(request):
    try:
        lab = Lab.objects.get(lab_id=request.user)  
        requests = LabOrderRequest.objects.filter(lab=lab)  
    except Lab.DoesNotExist:
        requests = None  

    return render(request, 'lab/lab_requests.html', {'requests': requests})



def leave_review(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    
    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            appointment=appointment,
            patient=appointment.patient,
            dentist=appointment.dentist,
            rating=rating,
            comment=comment
        )
      
        appointment.status = "Reviewed"
        appointment.save()

        return redirect('patient_bookings')  
    
    return render(request, 'patient/leave_review.html', {'appointment': appointment})

def view_reviews(request):
    reviews = Review.objects.all()
    return render(request, 'admin/admin_reviews.html', {'reviews': reviews})

def admin_lab_orders(request):
    lab_orders = LabOrder.objects.all()
    lab_order_requests = LabOrderRequest.objects.all()
    return render(request, 'admin/admin_lab_orders.html', {'lab_orders': lab_orders, 'lab_order_requests': lab_order_requests})

def patient_profile(request):
    patient = Patient.objects.get(patient_id=request.user)  
    return render(request, 'patient/patient_profile.html', {'patient': patient})

def dentist_profile(request):
    dentist = Dentist.objects.get(dentist_id=request.user)
    return render(request, 'dentist/dentist_profile.html', {'dentist': dentist})

def lab_profile(request):
    lab = Lab.objects.get(lab_id=request.user)
    return render(request, 'lab/lab_profile.html', {'lab': lab})

def view_dentist_reviews(request, dentist_id):
    dentist = get_object_or_404(Dentist, id=dentist_id)
    reviews = Review.objects.filter(dentist=dentist).select_related('patient')

    return render(request, 'patient/dentist_reviews.html', {
        'dentist': dentist,
        'reviews': reviews
    })


from django.shortcuts import render, redirect
from .models import Review, Patient

def patient_reviews(request):
    if not request.user.is_authenticated:
        return redirect('view_login')  

    try:
        patient = Patient.objects.get(patient_id=request.user)  # Fetch the patient linked to the logged-in user
        reviews = Review.objects.filter(patient=patient)
    except Patient.DoesNotExist:
        reviews = []  # No patient found, so no reviews to display

    return render(request, 'patient/view_reviews.html', {'reviews': reviews})
