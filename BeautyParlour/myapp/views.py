from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import *
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from datetime import datetime as dt
import re
from django.contrib import messages


# Create your views here.

def index(request):
    return render(request,'index.html')


def register_expert(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        expertise = request.POST.get('expertise')
        experience = request.POST.get('experience')
        file = request.FILES.get('file')

        # Email validation: must end with .com or .in
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|in)$'
        if not re.match(email_pattern, email):
            messages.error(request, 'Invalid email. It must end with .com or .in')
            return redirect('/register_expert')

        # Check if the username (email) already exists
        if Login.objects.filter(username=email).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return redirect('/register_expert')

        # Create the new user
        user = Login.objects.create_user(username=email, password=password, view_password=password, usertype='Expert')
        user.save()

        # Create the associated Expert profile
        expert = Expert(
            login_id=user, name=username, email=email, contact=contact, 
            address=address, experience=experience, expertise=expertise, file=file
        )  
        expert.save()

        messages.success(request, 'Expert Registration Successful.')
        return redirect('/viewExperts')

    return render(request, 'ADMIN/register_expert.html')






def register_customer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        file = request.FILES.get('file')

        # Email validation regex for @gmail.com or @gmail.in
        email_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.(com|in)$"
        
        if not re.match(email_pattern, email):
            messages.error(request, 'Email must be a valid Gmail address ending in .com or .in')
            return redirect('/register_customer')

        # Check if the username already exists
        if Login.objects.filter(username=email).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return redirect('/register_customer')

        # Create the new user
        user = Login.objects.create_user(username=email, password=password, view_password=password, usertype='Customer', is_active=True)
        user.save()

        # Create the associated Customer profile
        customer = Customer(login_id=user, name=username, email=email, contact=contact, address=address, file=file)
        customer.save()

        messages.success(request, 'Customer Registration Successful. You can now login.')
        return redirect('/login')

    return render(request, 'register_customer.html')


from django.contrib.auth import authenticate, login as auth_login
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log the user in
            auth_login(request, user)
            
            # Redirect based on user type
            if user.usertype == 'admin':
                messages.success(request, 'Welcome to the admin page!')
                return redirect('/adminHome')
            elif user.usertype == 'Customer':
                request.session['uid'] = user.id
                messages.success(request, 'Welcome to the Customer page!')
                return redirect('/customerHome')
            elif user.usertype == 'Expert':
                request.session['uid'] = user.id
                messages.success(request, 'Welcome to the Expert page!')
                return redirect('/expertHome')
            else:
                messages.error(request, 'Invalid user type.')
                return redirect('/login')
        else:
            # Invalid credentials
            messages.error(request, 'Invalid email or password.')
            return redirect('/login')
        
    # Render the login page for GET requests
    return render(request, 'login.html')


# ADMIN
def adminHome(request):
    return render(request, 'ADMIN/adminHome.html')  

def expertHome(request):
    return render(request, 'EXPERT/expertHome.html')  

def viewCustomers(request):
    customers = Customer.objects.all()
    print(customers)
    return render(request, 'ADMIN/viewCustomers.html', {'customers': customers})

def deleteCustomer(request):
    id = request.GET.get('id')
    Login.objects.get(id=id).delete()
    messages.error(request, 'User Deleted.')
    return redirect('/viewCustomers')

def viewExperts(request):
    experts = Expert.objects.all()
    print(experts)
    return render(request, 'ADMIN/viewExperts.html', {'experts': experts})

def deleteExperts(request):
    id = request.GET.get('id')
    Login.objects.get(id=id).delete()
    messages.error(request, 'Expert Deleted.')
    return redirect('/viewExperts')

def adminViewServices(request):
    services = Service.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        category = request.POST.get('category')
        service = Service(name=name, price=price, description=description, file=file, category=category)
        service.save()
        messages.success(request, 'Service Added.')
        return redirect('/adminViewServices')
    return render(request, 'ADMIN/adminViewServices.html', {'services': services})

def deleteService(request):
    id = request.GET.get('id')
    Service.objects.get(id=id).delete()
    messages.error(request, 'Service Deleted.')
    return redirect('/adminViewServices')


def addPackage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        category = request.POST.get('category') 
        service = Service(name=name, price=price, description=description, file=file, category=category)
        service.save()
        messages.success(request, 'Service Added.')
        return redirect('/addPackage')
    return render(request, 'ADMIN/addPackage.html')



# CUSTOMER

def customerHome(request): 
    services = Service.objects.all()
    if request.user.is_authenticated:
        booked_services_ids = Bookings.objects.filter(customer__login_id=request.user, payment_status='Paid').values_list('service_id', flat=True)
    else:
        booked_services_ids = []
    return render(request, 'CUSTOMER/customerHome.html', {'services': services, 'booked_services_ids': booked_services_ids})



def payment_page(request, service_id):
    if not request.user.is_authenticated:
        return redirect('login')

    service = Service.objects.get(id=service_id)
    customer = Customer.objects.get(login_id=request.user)
    selected_date = request.GET.get('date')  

    if request.method == "POST":
        Bookings.objects.create(
            customer=customer, 
            service=service, 
            payment_status="Paid",
            scheduled_date=selected_date  # Save the date
        )
        return redirect('booking_success')

    return render(request, "CUSTOMER/payment_page.html", {"service": service, "selected_date": selected_date})


def booking_success(request):
    return render(request, "CUSTOMER/booking_success.html")


def add_skintone(request):
    customer = Customer.objects.get(login_id=request.user)

    if request.method == "POST":
        skintone_image = request.FILES.get("skintone")
        # skintone_type = request.POST.get("skintone_type")  

        if skintone_image:
           
            Skin.objects.create(
                customer_id=customer,
                # skintone=skintone_type,
                skintone_image=skintone_image
            )
            return redirect("/customerHome")  

    return render(request, "CUSTOMER/add_skintone.html")


def view_bookings(request):
    if request.user.is_authenticated and request.user.usertype == 'admin':  
        bookings = Bookings.objects.all().select_related('customer', 'service', 'assigned_expert')  
        experts = Expert.objects.all()
        return render(request, 'admin/view_bookings.html', {'bookings': bookings, 'experts': experts})
    else:
        return redirect('login')

def assign_expert(request, booking_id):
    if request.user.is_authenticated and request.user.usertype == 'admin':
        if request.method == 'POST':
            expert_id = request.POST.get('expert_id')
            booking = Bookings.objects.get(id=booking_id)
            expert = Expert.objects.get(id=expert_id)
            booking.assigned_expert = expert
            booking.save()
            return redirect('view_bookings')  # Redirect back to the bookings page
    else:
        return redirect('login')



def schedule_service(request, booking_id): 
    if request.method == 'POST':
        service_time = request.POST.get('service_time')

        if not service_time:
            return HttpResponse("Invalid Time input!", status=400)

        booking = get_object_or_404(Bookings, id=booking_id)

        if not booking.scheduled_date:  # Ensure the customer has set a date
            return HttpResponse("Customer has not selected a scheduled date!", status=400)
        
        time_obj = datetime.strptime(service_time, "%H:%M").time()

        
        booking.time_schedule = time_obj
        booking.save()

        return redirect('view_bookings')

    return redirect('admin_dashboard')




def customer_bookings(request):    
    if not request.user.is_authenticated:
        return redirect('login') 
    try:
        customer = Customer.objects.get(login_id=request.user)
    except Customer.DoesNotExist:
        customer = None  
    
    if customer:
        customer_bookings = Bookings.objects.filter(customer=customer)
    else:
        customer_bookings = []  
    
    return render(request, 'CUSTOMER/customer_bookings.html', {'bookings': customer_bookings})




def view_skins(request):
    customer = get_object_or_404(Customer, login_id=request.user)
    skins = Skin.objects.filter(customer_id=customer)

    return render(request, 'CUSTOMER/view_skins.html', {'skins': skins})


def chat(request):
    uid = request.session["uid"]
    name = ""
    artistData = Customer.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(sellerid__login_id=uid) & Q(customerid=id))
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    userid = Expert.objects.get(login_id=uid)
    if id:
        customerid = Customer.objects.get(id=id)
        name = customerid.name
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            sellerid=userid, message=message, customerid=customerid, time=formatted_time, utype="SELLER")
        sendMsg.save()
    return render(request, "EXPERT/reply.html", {"artistData": artistData, "getChatData": getChatData, "customerid": name, "id": id})


def reply(request):
    uid = request.session["uid"]
    name = ""
    userData = Expert.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(customerid__login_id=uid) & Q(sellerid=id))
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    customerid = Customer.objects.get(login_id=uid)
    if id:
        userid = Expert.objects.get(id=id)
        name = userid.name
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            sellerid=userid, message=message, customerid=customerid, time=formatted_time, utype="CUSTOMER")
        sendMsg.save()
    return render(request, "CUSTOMER/chat.html", {"userData": userData, "getChatData": getChatData, "userid": name, "id": id})


def expert_assigned_customers(request):
    if request.user.is_authenticated and request.user.usertype == 'Expert':  
        expert = Expert.objects.get(login_id=request.user)
        bookings = Bookings.objects.filter(assigned_expert=expert).select_related('customer', 'service')
        return render(request, 'expert/assigned_customers.html', {'bookings': bookings})
    else:
        return redirect('login')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from .models import Skin, Customer

def all_skins(request):
    skins = Skin.objects.all()  # Fetch all skin records
    return render(request, 'ADMIN/all_skins.html', {'skins': skins})

def update_skin_tone(request, skin_id):
    if request.method == "POST":
        skintone = request.POST.get("skintone")
        skin = get_object_or_404(Skin, id=skin_id)
        skin.skintone = skintone  # Update skin tone
        skin.save()
        messages.success(request, f"Skin tone updated for {skin.customer_id.name}!")
    return redirect('/all_skins')

def send_skin_message(request, skin_id):
    if request.method == 'POST':
        message = request.POST.get('message')
        skin = get_object_or_404(Skin, id=skin_id)
        customer = skin.customer_id

        if not customer.email:
            messages.error(request, 'Customer does not have an email address.')
            return redirect('/all_skins')

        # Send email
        send_mail(
            subject=f"Skin Treatment Advice for {customer.name}",
            message=message,
            from_email="admin@example.com",  # Replace with your email
            recipient_list=[customer.email],
            fail_silently=False
        )

        messages.success(request, f"Message sent to {customer.name} successfully!")
    return redirect('/all_skins')

##############################################################################################################
def udp(request):
    Login.objects.filter(id=5).delete()
    return HttpResponse("Under Development Page")


def dlt(request):
    data=Login.objects.filter(id="12").delete()
    return redirect('/')