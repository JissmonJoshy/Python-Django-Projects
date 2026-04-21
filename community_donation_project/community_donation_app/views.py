from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout
from django.db.models import Q
from datetime import datetime as dt
from django.db.models import Avg, Count, Sum

# Create your views here.
def index(request):
    donations = Donation.objects.all()
    return render(request,'index.html',{'donations':donations})


def admin_dashboard(request):
    donations = Donation.objects.all()
    return render(request,'admin/admin_dashboard.html',{'donations':donations})

def donor_dashboard(request):
    donations = Donation.objects.all()
    return render(request,'donor/donor_dashboard.html',{'donations':donations})

def ngo_dashboard(request):
    donations = Donation.objects.all()
    return render(request,'ngo/ngo_dashboard.html',{'donations':donations})


def user_logout(request):
    logout(request)
    return redirect('index')


def view_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']       
        
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            if user.is_active:             
                auth_login(request, user)
                request.session['user_id'] = user.id             
                
                if user.is_superuser:
                    return redirect('admin_dashboard')  

                elif user.usertype == "Donor":
                    return redirect('donor_dashboard')
                
                elif user.usertype == "NGO":
                    return redirect('ngo_dashboard')

                else:
                    return redirect('login') 
                
            else:
                messages.error(request, 'Your account is inactive')
                return render(request, 'login.html')
            
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
        
    return render(request, 'login.html')


def donor_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        image = request.FILES.get('image')

        if Login.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('donor_register')

        if Login.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('donor_register')

        if Donor.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number is already registered.')
            return redirect('donor_register')

        login_user = Login.objects.create(
            username=username,
            usertype="Donor",
            email=email,
            viewpassword=password,
            is_active=False  # Donor waiting for admin approval
        )
        login_user.set_password(password)
        login_user.save()

        donor = Donor.objects.create(
            donor_id=login_user,
            username=username,
            name=name,
            email=email,
            phone=phone,
            address=address,
            image=image
        )
        donor.save()

        messages.success(request, 'Donor registered successfully! Waiting for admin approval.')
        return redirect('donor_register')

    return render(request, 'donor/donor_register.html')



def ngo_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        image = request.FILES.get('image')

        # Check if the username, email, or phone already exists
        if Login.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('ngo_register')

        if Login.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('ngo_register')

        if Ngo.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number is already registered.')
            return redirect('ngo_register')

        # Create Login user object
        login_user = Login.objects.create(
            username=username,
            usertype="NGO",
            email=email,
            viewpassword=password,
            is_active=False  # Set to False for admin approval
        )
        login_user.set_password(password)
        login_user.save()

        # Create NGO profile
        ngo = Ngo.objects.create(
            ngo_id=login_user,
            username=username,
            name=name,
            email=email,
            phone=phone,
            address=address,
            image=image
        )
        ngo.save()

        messages.success(request, 'NGO registered successfully! Waiting for admin approval.')
        return redirect('ngo_register')  
    return render(request, 'ngo/ngo_register.html')


def display_all_donor(request):
    donors = Donor.objects.all()
    return render(request,'admin/display_all_donor.html',{'donors':donors})


def display_all_ngo(request):
    ngos = Ngo.objects.all()
    return render(request,'admin/display_all_ngo.html',{'ngos':ngos})


def my_donations(request):
    try:
        donor = Donor.objects.get(donor_id=request.user)
        transactions = DonationTransaction.objects.filter(donor=donor)
    except Donor.DoesNotExist:
        transactions = []  
    return render(request, 'donor/my_donations.html', {'transactions': transactions})



def view_donation_transactions(request):
    transactions = DonationTransaction.objects.all()
    return render(request, 'admin/view_donation_transactions.html', {'transactions': transactions})



def approve_donor(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    login_user = donor.donor_id  
    login_user.is_active = True  
    login_user.save()
    messages.success(request, f"User {donor.username} has been approved!")
    return redirect('display_all_donor')

def reject_donor(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    login_user = donor.donor_id  
    donor.delete()  
    login_user.delete() 
    messages.success(request, f"User {donor.username} has been rejected and removed!")
    return redirect('display_all_donor')

def delete_donor(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    login_user = donor.donor_id 

    if login_user.is_active:  
        donor.delete()
        login_user.delete()
        messages.success(request, f"User {donor.username} has been deleted successfully!")
    else:
        messages.error(request, "You cannot delete a user who is not yet approved!")
    
    return redirect('display_all_donor')


def approve_ngo(request, ngo_id):
    ngo = get_object_or_404(Ngo, id=ngo_id)
    login_user = ngo.ngo_id  
    login_user.is_active = True  
    login_user.save()
    messages.success(request, f"NGO {ngo.username} has been approved!")
    return redirect('display_all_ngo')


def reject_ngo(request, ngo_id):
    ngo = get_object_or_404(Ngo, id=ngo_id)
    login_user = ngo.ngo_id  
    ngo.delete()
    login_user.delete()
    messages.success(request, f"NGO {ngo.username} has been rejected and removed!")
    return redirect('display_all_ngo')


def delete_ngo(request, ngo_id):
    ngo = get_object_or_404(Ngo, id=ngo_id)
    login_user = ngo.ngo_id  
    
    if login_user.is_active:  
        ngo.delete()
        login_user.delete()
        messages.success(request, f"NGO {ngo.username} has been deleted successfully!")
    else:
        messages.error(request, "You cannot delete an NGO that is not yet approved!")
    
    return redirect('display_all_ngo')


@login_required
def view_profile_ngo(request):    
    logged_in_user = request.user
    try:
        ngo_profile = Ngo.objects.get(ngo_id=logged_in_user)
    except Ngo.DoesNotExist:
        ngo_profile = None 
    return render(request, 'ngo/view_profile_ngo.html', {'ngo_profile': ngo_profile})



@login_required
def edit_profile_ngo(request):
    logged_in_user = request.user

    try:
        ngo_profile = Ngo.objects.get(ngo_id=logged_in_user)
    except Ngo.DoesNotExist:
        return redirect('view_profile_ngo')  

    if request.method == "POST":
        new_username = request.POST.get('username')
        new_name = request.POST.get('name')
        new_email = request.POST.get('email')
        new_phone = request.POST.get('phone')
        new_address = request.POST.get('address')

        ngo_profile.username = new_username
        ngo_profile.name = new_name
        ngo_profile.email = new_email
        ngo_profile.phone = new_phone
        ngo_profile.address = new_address

        
        logged_in_user.username = new_username  
        logged_in_user.save()  

        
        if 'image' in request.FILES:
            ngo_profile.image = request.FILES['image']

        ngo_profile.save()  
        return redirect('view_profile_ngo')  

    return render(request, 'ngo/edit_profile_ngo.html', {'ngo_profile': ngo_profile})




@login_required
def add_donation(request):
    logged_in_user = request.user
    try:
        ngo_profile = Ngo.objects.get(ngo_id=logged_in_user)
    except Ngo.DoesNotExist:
        messages.error(request, "You need to set up your NGO profile first.")
        return redirect('view_profile_ngo')

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        donation_type = request.POST.get('donation_type', 'Monetary')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        location = request.POST.get('location')
        status = request.POST.get('status', 'Active')

        # Handle target_amount properly
        target_amount = request.POST.get('target_amount')
        target_amount = int(target_amount) if target_amount else None  # Convert to int or set None

        donation = Donation(
            ngo=ngo_profile,
            title=title,
            description=description,
            category=category,
            target_amount=target_amount,
            current_amount=0 if target_amount else None,  # Make current_amount None if no target amount
            donation_type=donation_type,
            start_date=start_date,
            end_date=end_date,
            location=location,
            status=status
        )
        if 'image' in request.FILES:
            donation.image = request.FILES['image']

        donation.save()
        messages.success(request, "Donation added successfully!")
        return redirect('add_donation')  
    return render(request, 'ngo/add_donation.html')




@login_required
def view_donations(request):
    logged_in_user = request.user
    try:
        ngo_profile = Ngo.objects.get(ngo_id=logged_in_user)
    except Ngo.DoesNotExist:
        return redirect('view_profile_ngo')
    donations = Donation.objects.filter(ngo=ngo_profile)
    return render(request, 'ngo/view_donations.html', {'donations': donations})



@login_required
def edit_donation(request, donation_id):
    logged_in_user = request.user
    try:
        ngo_profile = Ngo.objects.get(ngo_id=logged_in_user)
    except Ngo.DoesNotExist:
        return redirect('view_profile_ngo')
    try:
        donation = Donation.objects.get(id=donation_id, ngo=ngo_profile)
    except Donation.DoesNotExist:
        messages.error(request, "Donation not found or you are not authorized to edit it.")
        return redirect('view_donations')

    if request.method == "POST":
        donation.title = request.POST.get('title')
        donation.description = request.POST.get('description')
        donation.category = request.POST.get('category')
        donation.target_amount = request.POST.get('target_amount')
        donation.current_amount = request.POST.get('current_amount')
        donation.start_date = request.POST.get('start_date')
        donation.end_date = request.POST.get('end_date')
        donation.location = request.POST.get('location')
        donation.status = request.POST.get('status')

        if 'image' in request.FILES:
            donation.image = request.FILES['image']

        donation.save()
        messages.success(request, "Donation updated successfully!")
        return redirect('view_donations')
    return render(request, 'ngo/edit_donation.html', {'donation': donation})


@login_required
def delete_donation(request, donation_id):
    logged_in_user = request.user

    try:
        ngo_profile = Ngo.objects.get(ngo_id=logged_in_user)
    except Ngo.DoesNotExist:
        return redirect('view_profile_ngo')

    try:
        donation = Donation.objects.get(id=donation_id, ngo=ngo_profile)
    except Donation.DoesNotExist:
        messages.error(request, "Donation not found or you are not authorized to delete it.")
        return redirect('view_donations')

    donation.delete()
    messages.success(request, "Donation deleted successfully!")
    return redirect('view_donations')



@login_required
def view_profile_donor(request):
    logged_in_user = request.user
    
    try:
        donor_profile = Donor.objects.get(donor_id=logged_in_user)
    except Donor.DoesNotExist:   
        return redirect('view_profile_donor') 
    return render(request, 'donor/view_profile_donor.html', {'donor_profile': donor_profile})


@login_required
def edit_profile_donor(request):
    donor_profile = Donor.objects.get(donor_id=request.user)
    
    if request.method == 'POST':
        donor_profile.username = request.POST.get('username')
        donor_profile.name = request.POST.get('name')
        donor_profile.email = request.POST.get('email')
        donor_profile.phone = request.POST.get('phone')
        donor_profile.address = request.POST.get('address')
        
        if request.FILES.get('image'):
            donor_profile.image = request.FILES['image']
        
        donor_profile.save()

        login_user = donor_profile.donor_id
        login_user.username = donor_profile.username
        login_user.email = donor_profile.email
        login_user.save()

        messages.success(request, "Profile updated successfully!")

        return redirect('view_profile_donor')

    return render(request, 'donor/edit_profile_donor.html', {'donor_profile': donor_profile})

@login_required
def display_all_donations(request): 
    donations = Donation.objects.all()
    return render(request, 'donor/display_all_donations.html', {'donations': donations})


@login_required
def make_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    donor = get_object_or_404(Donor, donor_id=request.user)

    if request.method == 'POST':
        donation_type = request.POST.get('donation_type')
        amount = request.POST.get('amount') if request.POST.get('amount') else None
        payment_method = request.POST.get('payment_method') if request.POST.get('payment_method') else None

        if donation_type == 'Monetary':
            if not amount or not payment_method:
                messages.error(request, "Please enter amount and select a payment method.")
                return redirect('make_donation', donation_id=donation.id)

            amount = int(amount)
            if payment_method == 'card':
                card_number = request.POST.get('card_number')
                card_holder = request.POST.get('card_holder')
                expiry_date = request.POST.get('expiry_date')
                cvv = request.POST.get('cvv')

                if not (card_number and card_holder and expiry_date and cvv):
                    messages.error(request, "Please fill in all card details.")
                    return redirect('make_donation', donation_id=donation.id)

            if donation.current_amount is None:
                donation.current_amount = 0
            donation.current_amount += amount
            donation.save()

      
        DonationTransaction.objects.create(
            donor=donor,
            donation=donation,
            donation_type=donation_type,
            amount=amount if donation_type == 'Monetary' else None,
            payment_method=payment_method if donation_type == 'Monetary' else None
        )

        messages.success(request, "Donation successful!")
        return redirect('display_all_donations')

    return render(request, 'donor/make_donation.html', {'donation': donation})



@login_required
def admin_view_donations(request):
    donations = Donation.objects.all()
    return render(request, 'admin/admin_view_donations.html', {'donations': donations})


@login_required
def deactivate_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    
    if donation.current_amount >= donation.target_amount:
        donation.status = "Deactive"
        donation.save()
    
    return redirect('view_donations')


@login_required
def ngo_donations_received(request):
    try:
        logged_in_ngo = Ngo.objects.get(ngo_id=request.user)  
        donations_received = DonationTransaction.objects.filter(donation__ngo=logged_in_ngo)
    except Ngo.DoesNotExist:
        donations_received = []
    return render(request, 'ngo/ngo_donations_received.html', {'donations_received': donations_received})




def chat(request):
    uid = request.session["user_id"]
    name = ""
    ngoData = Ngo.objects.all()
    
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(donor_id__donor_id=uid) & Q(ngo_id=id)
    )
    
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    donor_id = Donor.objects.get(donor_id=uid)
    
    if id:
        userid = Ngo.objects.get(id=id)
        name = userid.name

    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            ngo_id=userid, message=message, donor_id=donor_id, time=formatted_time, utype="Donor"
        )
        sendMsg.save()

    return render(request, "donor/chat.html", {"ngoData": ngoData, "getChatData": getChatData, "userid": name, "id": id})


def reply(request):
    uid = request.session["user_id"]
    name = ""
    donorData = Donor.objects.all()
    
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(ngo_id__ngo_id=uid) & Q(donor_id=id)
    )
    
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    ngo_id = Ngo.objects.get(ngo_id=uid)

    if id:
        userid = Donor.objects.get(id=id)
        name = userid.name

    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            donor_id=userid, message=message, ngo_id=ngo_id, time=formatted_time, utype="Ngo"
        )
        sendMsg.save()

    return render(request, "ngo/reply.html", {"donorData": donorData, "getChatData": getChatData, "userid": name, "id": id})



@login_required
def generate_report(request):
    donations = Donation.objects.all()
    
    donation_titles = []
    avg_amounts = []

    for donation in donations:
        
        donation_data = DonationTransaction.objects.filter(donation=donation).aggregate(
            total_amount=Sum('amount'),
            unique_donors=Count('donor', distinct=True)
        )
        
        total_amount = donation_data['total_amount'] or 0
        unique_donors = donation_data['unique_donors'] or 1  

        avg_amount_per_donor = total_amount / unique_donors
        donation_titles.append(donation.title)
        avg_amounts.append(avg_amount_per_donor)

    total_donors = DonationTransaction.objects.values('donor').distinct().count()

    context = {
        'donation_titles': donation_titles,
        'avg_amounts': avg_amounts,
        'total_donors': total_donors  
    }
    
    return render(request, 'admin/generate_report.html', context)
