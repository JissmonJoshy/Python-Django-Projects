from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
import re
from django.contrib.auth.hashers import make_password


# Create your views here.
def adm(request):
    adm=Login.objects.create_superuser(username='admin',email='admin@gmail.com',viewpassword='1234',password='1234',usertype='Admin')
    adm.save()
    return redirect('/')

def dlt(request):
    Checkout.objects.filter(id="1").delete()
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
                    messages.success(request, 'Welcome to Admin Dashboard')
                    return redirect('admin_dashboard')

                elif user.usertype == "User":
                    request.session['uid'] = user.id
                    messages.success(request, 'Welcome to User Dashboard')
                    return redirect('user_dashboard')
                
                elif user.usertype == "Farmer":
                    request.session['uid'] = user.id
                    messages.success(request, 'Welcome to Farmer Dashboard')
                    return redirect('farmer_dashboard')
                
                elif user.usertype == "Delivery":
                    request.session['uid'] = user.id
                    messages.success(request, 'Welcome to Delivery Dashboard')
                    return redirect('delivery_dashboard')
                
                else:
                    return redirect('logins')  
            else:
                messages.error(request, 'Your account is inactive')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')

def user_dashboard(request):
    products = Product.objects.filter(status='accepted')
    return render(request, 'user/user_dashboard.html', {'products': products})


def delivery_dashboard(request):
    return render(request,'delivery/delivery_dashboard.html')

def farmer_dashboard(request):
    return render(request,'farmer/farmer_dashboard.html')



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
            is_active=False,
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






def delivery_register(request):
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
            return redirect("delivery_register")

        if not re.match(domain_pattern, email):
            messages.error(request, "Email must have a .in or .com domain.")
            return redirect("delivery_register")

        if not re.match(phone_pattern, phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect("delivery_register")

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect("delivery_register")

        if Login.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect("delivery_register")

        if Delivery.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number is already registered.")
            return redirect("delivery_register")

        login_user = Login.objects.create(
            username=username,
            password=make_password(password),
            usertype="Delivery",
            email=email,
            viewpassword=password,
            is_active=False,
        )

        Delivery.objects.create(
            user=login_user,
            username=username,
            name=name,
            address=address,
            phone=phone,
            email=email,
            image=image
        )

        messages.success(request, "Delivery Agent registered successfully!")
        return redirect("view_login")

    return render(request, "delivery_register.html")





def farmer_register(request):
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
            return redirect("farmer_register")

        if not re.match(domain_pattern, email):
            messages.error(request, "Email must have a .in or .com domain.")
            return redirect("farmer_register")

        if not re.match(phone_pattern, phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect("farmer_register")

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect("farmer_register")

        if Login.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect("farmer_register")

        if Farmer.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number is already registered.")
            return redirect("farmer_register")

        login_user = Login.objects.create(
            username=username,
            password=make_password(password),
            usertype="Farmer",
            email=email,
            viewpassword=password,
            is_active=False,
        )

        Farmer.objects.create(
            user=login_user,
            username=username,
            name=name,
            address=address,
            phone=phone,
            email=email,
            image=image
        )

        messages.success(request, "FArmer registered successfully!")
        return redirect("view_login")

    return render(request, "farmer_register.html")


def view_registered_users(request):
    users = User.objects.all()
    return render(request, 'admin/view_registered_users.html', {'users': users})
   
def accept_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.user.is_active = True
    user.user.save()
    messages.success(request, "User approved successfully!")
    return redirect('view_registered_users')

def reject_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.user.is_active = False
    user.user.save()
    messages.warning(request, "User rejected!")
    return redirect('view_registered_users')

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.user.delete()
    messages.error(request, "User deleted successfully!")
    return redirect('view_registered_users')

def view_registered_farmers(request):
    farmers = Farmer.objects.all()
    return render(request, 'admin/view_registered_farmers.html', {'farmers': farmers})

def accept_farmer(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)
    farmer.user.is_active = True
    farmer.user.save()
    messages.success(request, "Farmer approved successfully!")
    return redirect('view_registered_farmers')

def reject_farmer(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)
    farmer.user.is_active = False
    farmer.user.save()
    messages.warning(request, "Farmer rejected!")
    return redirect('view_registered_farmers')

def delete_farmer(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)
    farmer.user.delete()
    messages.error(request, "Farmer deleted successfully!")
    return redirect('view_registered_farmers')


def view_registered_delivery(request):
    delivery_agents = Delivery.objects.all()
    return render(request, 'admin/view_registered_delivery.html', {'delivery_agents': delivery_agents})


def accept_delivery(request, delivery_id):
    delivery_agent = get_object_or_404(Delivery, id=delivery_id)
    delivery_agent.user.is_active = True
    delivery_agent.user.save()
    messages.success(request, "Delivery agent approved successfully!")
    return redirect('view_registered_delivery')


def reject_delivery(request, delivery_id):
    delivery_agent = get_object_or_404(Delivery, id=delivery_id)
    delivery_agent.user.is_active = False
    delivery_agent.user.save()
    messages.warning(request, "Delivery agent rejected!")
    return redirect('view_registered_delivery')


def delete_delivery(request, delivery_id):
    delivery_agent = get_object_or_404(Delivery, id=delivery_id)
    delivery_agent.user.delete()
    messages.error(request, "Delivery agent deleted successfully!")
    return redirect('view_registered_delivery')


def view_profile_farmer(request):
    farmer = Farmer.objects.get(user=request.user)
    return render(request, 'farmer/view_profile_farmer.html', {'farmer': farmer})

def edit_profile_farmer(request):
    farmer = Farmer.objects.get(user=request.user)

    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']

        email_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
        domain_pattern = r".+\.(in|com)$"
        phone_pattern = r"^\d{10}$"

        if not re.match(email_pattern, email):
            messages.error(request, "Only Gmail addresses are allowed.")
            return redirect("edit_profile_farmer")

        if not re.match(domain_pattern, email):
            messages.error(request, "Email must have a .in or .com domain.")
            return redirect("edit_profile_farmer")

        if not re.match(phone_pattern, phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect("edit_profile_farmer")

        if Login.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.error(request, "Username is already taken.")
            return redirect("edit_profile_farmer")

        if Login.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, "Email is already in use.")
            return redirect("edit_profile_farmer")

        if Farmer.objects.filter(phone=phone).exclude(id=farmer.id).exists():
            messages.error(request, "Phone number is already registered.")
            return redirect("edit_profile_farmer")

        # Update Farmer model
        farmer.name = name
        farmer.username = username
        farmer.email = email
        farmer.address = address
        farmer.phone = phone

        if 'image' in request.FILES:
            farmer.image = request.FILES['image']
        farmer.save()

        # Update Login model
        request.user.username = username
        request.user.email = email
        request.user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('view_profile_farmer')

    return render(request, 'farmer/edit_profile_farmer.html', {'farmer': farmer})



def view_profile_delivery(request): 
    delivery = Delivery.objects.get(user=request.user)
    return render(request, 'delivery/view_profile_delivery.html', {'delivery': delivery})


def edit_profile_delivery(request):
    delivery = Delivery.objects.get(user=request.user)

    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']

        email_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
        domain_pattern = r".+\.(in|com)$"
        phone_pattern = r"^\d{10}$"

        if not re.match(email_pattern, email):
            messages.error(request, "Only Gmail addresses are allowed.")
            return redirect("edit_profile_delivery")

        if not re.match(domain_pattern, email):
            messages.error(request, "Email must have a .in or .com domain.")
            return redirect("edit_profile_delivery")

        if not re.match(phone_pattern, phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect("edit_profile_delivery")

        if Login.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.error(request, "Username is already taken.")
            return redirect("edit_profile_delivery")

        if Login.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, "Email is already in use.")
            return redirect("edit_profile_delivery")

        if Delivery.objects.filter(phone=phone).exclude(id=delivery.id).exists():
            messages.error(request, "Phone number is already registered.")
            return redirect("edit_profile_delivery")

        delivery.name = name
        delivery.username = username
        delivery.email = email
        delivery.address = address
        delivery.phone = phone

        if 'image' in request.FILES:
            delivery.image = request.FILES['image']
        delivery.save()

        request.user.username = username
        request.user.email = email
        request.user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('view_profile_delivery')

    return render(request, 'delivery/edit_profile_delivery.html', {'delivery': delivery})


def view_profile_user(request): 
    user_profile = User.objects.get(user=request.user)
    return render(request, 'user/view_profile_user.html', {'user_profile': user_profile})


def edit_profile_user(request):
    user_profile = User.objects.get(user=request.user)

    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']

        email_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
        domain_pattern = r".+\.(in|com)$"
        phone_pattern = r"^\d{10}$"

        if not re.match(email_pattern, email):
            messages.error(request, "Only Gmail addresses are allowed.")
            return redirect("edit_profile_user")

        if not re.match(domain_pattern, email):
            messages.error(request, "Email must have a .in or .com domain.")
            return redirect("edit_profile_user")

        if not re.match(phone_pattern, phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect("edit_profile_user")

        if Login.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.error(request, "Username is already taken.")
            return redirect("edit_profile_user")

        if Login.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, "Email is already in use.")
            return redirect("edit_profile_user")

        if User.objects.filter(phone=phone).exclude(id=user_profile.id).exists():
            messages.error(request, "Phone number is already registered.")
            return redirect("edit_profile_user")

        user_profile.name = name
        user_profile.username = username
        user_profile.email = email
        user_profile.address = address
        user_profile.phone = phone

        if 'image' in request.FILES:
            user_profile.image = request.FILES['image']
        user_profile.save()

        request.user.username = username
        request.user.email = email
        request.user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('view_profile_user')

    return render(request, 'user/edit_profile_user.html', {'user_profile': user_profile})



def add_product(request):
    user = request.user
    farmer = Farmer.objects.get(user=user)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')

        Product.objects.create(
            farmer=farmer,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            image=image,
            status='pending'
        )
        messages.success(request, "Product added successfully.")
        return redirect('farmer_added_products')  # Or redirect somewhere else

    return render(request, 'farmer/add_product.html')


def farmer_added_products(request):
    user = request.user
    farmer = Farmer.objects.get(user=user)
    products = Product.objects.filter(farmer=farmer)

    return render(request, 'farmer/farmer_added_products.html', {'products': products})

def edit_product(request, pid):
    product = Product.objects.get(id=pid)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        return redirect('farmer_added_products')
    return render(request, 'farmer/edit_product.html', {'product': product})

def delete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    return redirect('farmer_added_products')


def farmer_orders(request):
    farmer = Farmer.objects.get(user=request.user)
    products = Product.objects.filter(farmer=farmer)
    checkout_items = CheckoutItem.objects.filter(product__in=products).select_related('checkout', 'product')

    # Get checkouts related to the farmer's products
    related_checkouts = set(item.checkout for item in checkout_items)
    return render(request, 'farmer/farmer_orders.html', {'checkouts': related_checkouts, 'checkout_items': checkout_items})


def farmer_reviews(request):
    farmer = Farmer.objects.get(user=request.user)
    products = Product.objects.filter(farmer=farmer)
    reviews = Review.objects.filter(product__in=products).select_related('product', 'user')
    return render(request, 'farmer/farmer_reviews.html', {'reviews': reviews})


def admin_products(request):
    products = Product.objects.all()
    return render(request, 'admin/admin_products.html', {'products': products})

def accept_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.status = 'accepted'
    product.save()
    return redirect('admin_products')

def reject_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.status = 'rejected'
    product.save()
    return redirect('admin_products')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'user/product_detail.html', {'product': product})

def add_to_favorite(request, product_id):
    if 'uid' in request.session:
        login_id = request.session['uid']
        product = get_object_or_404(Product, id=product_id)
        user = User.objects.get(user__id=login_id)

        Favorite.objects.get_or_create(user=user, product=product)
        messages.success(request, "Product added to favorites.")
    return redirect('view_favorites')

def view_favorites(request):
    if 'uid' in request.session:
        login_id = request.session['uid']
        user_obj = User.objects.get(user__id=login_id)
        favorites = Favorite.objects.filter(user=user_obj)
        return render(request, 'user/view_favorites.html', {'favorites': favorites})
    else:
        return redirect('logins')  
    
def remove_favorite(request, fav_id):
    Favorite.objects.filter(id=fav_id).delete()
    messages.success(request, "Favorite removed successfully.")
    return redirect('view_favorites')


def add_to_cart(request, product_id):
    if 'uid' in request.session:
        login_id = request.session['uid']
        user = get_object_or_404(User, user__id=login_id)
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            messages.warning(request, "Product is already added to cart.")
        else:
            messages.success(request, "Product added to cart successfully.")

        return redirect('view_cart')
    else:
        return redirect('logins')
        

def view_cart(request):
    login_id = request.session['uid']
    user = get_object_or_404(User, user__id=login_id)
    cart_items = Cart.objects.filter(user=user)
    return render(request, 'user/view_cart.html', {'cart_items': cart_items})


def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    product_stock = cart_item.product.quantity

    if cart_item.quantity < product_stock:
        cart_item.quantity += 1
        cart_item.save()
    else:
        messages.info(request, 'Cannot exceed available stock.')

    return redirect('view_cart')


def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')



def remove_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    return redirect('view_cart')

def checkout(request): 
    login_id = request.session['uid']
    user = get_object_or_404(User, user__id=login_id)
    cart_items = Cart.objects.filter(user=user)
    total = sum(item.subtotal() for item in cart_items)

    if request.method == 'POST':
        method = request.POST['payment_method']
        holder = request.POST.get('card_holder')
        number = request.POST.get('card_number')
        expiry = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        delivery_name = request.POST.get('delivery_name')
        delivery_phone = request.POST.get('delivery_phone')
        delivery_address = request.POST.get('delivery_address')
        delivery_pin = request.POST.get('delivery_pin')

        status = 'home delivery' if method == 'Home Delivery' else 'Paid'

        checkout = Checkout.objects.create(
            user=user,
            payment_method=method,
            card_holder=holder,
            card_number=number,
            expiry_date=expiry,
            cvv=cvv,
            total_amount=total,
            status=status,
            delivery_name=delivery_name,
            delivery_phone=delivery_phone,
            delivery_address=delivery_address,
            delivery_pin=delivery_pin
        )

        for item in cart_items:
            CheckoutItem.objects.create(
                checkout=checkout,
                product=item.product,
                quantity=item.quantity
            )
            item.product.quantity -= item.quantity
            item.product.save()

        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('view_cart')

    return render(request, 'user/checkout.html', {'cart_items': cart_items, 'total': total})




def view_checkout(request):
    login_id = request.session['uid']
    user = get_object_or_404(User, user__id=login_id)
    checkouts = Checkout.objects.filter(user=user).order_by('-created_at')
    return render(request, 'user/view_checkout.html', {'checkouts': checkouts})

def admin_view_all_checkouts(request):
    checkouts = Checkout.objects.all().order_by('-created_at')
    deliveries = Delivery.objects.filter(user__is_active=True, user__usertype='Delivery')
    return render(request, 'admin/admin_view_all_checkouts.html', {
        'checkouts': checkouts,
        'deliveries': deliveries
    })

    

def assign_delivery(request, checkout_id):
    if request.method == 'POST':
        delivery_id = request.POST['delivery_id']
        checkout = get_object_or_404(Checkout, id=checkout_id)
        delivery_user = get_object_or_404(Delivery, id=delivery_id)

        # You can add a field in Checkout model like `assigned_delivery = models.ForeignKey(Delivery, null=True, ...)`
        checkout.assigned_delivery = delivery_user
        checkout.save()
        messages.success(request, "Delivery assigned successfully.")
        return redirect('admin_view_all_checkouts')
    

def display_all_products(request):
    search_query = request.GET.get('search', '')
    order_by = request.GET.get('orderby', 'default')

    products = Product.objects.filter(status='accepted')

    if search_query:
        products = products.filter(name__icontains=search_query)

    if order_by == 'price':
        products = products.order_by('price')
    elif order_by == 'price-desc':
        products = products.order_by('-price')
    elif order_by == 'date':
        products = products.order_by('-id')  # assuming id reflects creation order

    context = {
        'products': products,
        'search_query': search_query,
        'order_by': order_by,
        'total_results': products.count()
    }
    return render(request, 'user/display_all_products.html', context)

def delivery_assigned_orders(request):
    delivery_user = request.user
    delivery = Delivery.objects.get(user=delivery_user)
    orders = Checkout.objects.filter(assigned_delivery=delivery)
    return render(request, 'delivery/delivery_assigned_orders.html', {'orders': orders})


def update_delivery_status(request, checkout_id):
    if request.method == 'POST':
        status = request.POST.get('delivery_status')
        checkout = Checkout.objects.get(id=checkout_id)
        checkout.delivery_status = status
        checkout.save()
        messages.success(request, "Delivery status updated successfully.")
        return redirect('delivery_assigned_orders')


def verify_payment_status(request, checkout_id):
    if request.method == 'POST':
        status = request.POST.get('payment_verification')
        checkout = Checkout.objects.get(id=checkout_id)
        checkout.payment_verification = status
        checkout.save()
        messages.success(request, "Payment status updated successfully.")
        return redirect('delivery_assigned_orders')


def submit_review(request, product_id):
    if request.method == 'POST':
        user_id = request.session['uid']
        user = User.objects.get(user__id=user_id)
        product = Product.objects.get(id=product_id)
        comment = request.POST['comment']
        rating = request.POST['rating']
        Review.objects.create(user=user, product=product, comment=comment, rating=rating)
        messages.success(request, "Review submitted successfully.")
    return redirect('view_checkout')



def view_reviews(request):
    login_id = request.session['uid']
    user = User.objects.get(user__id=login_id)
    reviews = Review.objects.filter(user=user).order_by('-created_at')
    return render(request, 'user/view_reviews.html', {'reviews': reviews})

def delete_review(request, review_id):
    login_id = request.session['uid']
    user = User.objects.get(user__id=login_id)
    review = get_object_or_404(Review, id=review_id, user=user)
    review.delete()
    messages.success(request, "Review deleted successfully.")
    return redirect('view_reviews')

from django.db.models import Sum
from django.shortcuts import render

def admin_product_analytics(request):
    chart_labels = []
    chart_values = []

    # Product orders (kg)
    products = Product.objects.all()
    for product in products:
        total_orders = CheckoutItem.objects.filter(product=product).aggregate(total=Sum('quantity'))['total'] or 0
        label = f"Product: {product.name} (₹{product.price}) - {product.farmer.name} - {total_orders} kg"
        chart_labels.append(label)
        chart_values.append(total_orders)

    # Supply orders (units)
    supplies = Supply.objects.all()
    for supply in supplies:
        total_orders = SupplyCheckoutItem.objects.filter(supply=supply).aggregate(total=Sum('quantity'))['total'] or 0
        label = f"Supply: {supply.name} ({supply.category}) - ₹{supply.price} - {total_orders} units"
        chart_labels.append(label)
        chart_values.append(total_orders)

    return render(request, 'admin/analytics.html', {
        'labels': chart_labels,
        'data': chart_values
    })



def add_supply(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        category = request.POST['category']
        price = request.POST['price']
        quantity = request.POST['quantity']
        image = request.FILES.get('image')

        supply = Supply(
            name=name,
            description=description,
            category=category,
            price=price,
            quantity=quantity,
            image=image
        )
        supply.save()
        messages.success(request, "Supply added successfully.")
        return redirect('add_supply')  # You can redirect to another page if needed

    return render(request, 'admin/add_supply.html')


def display_supply(request):
    supplies = Supply.objects.all().order_by('-created_at')
    return render(request, 'admin/display_supply.html', {'supplies': supplies})

def display_supply_farmer(request):
    search_query = request.GET.get('search', '')
    order_by = request.GET.get('orderby', 'default')

    supplies = Supply.objects.all()

    if search_query:
        supplies = supplies.filter(name__icontains=search_query)

    if order_by == 'price':
        supplies = supplies.order_by('price')
    elif order_by == 'price-desc':
        supplies = supplies.order_by('-price')
    elif order_by == 'date':
        supplies = supplies.order_by('-created_at')

    total_results = supplies.count()

    context = {
        'supplies': supplies,
        'total_results': total_results,
    }
    return render(request, 'farmer/display_supply_farmer.html', context)


def add_to_cart_supply(request, supply_id):
    supply = get_object_or_404(Supply, id=supply_id)
    farmer = Farmer.objects.get(user=request.user)

    existing_order = SupplyOrder.objects.filter(
        farmer=farmer,
        supply=supply,
        status='Pending'
    ).first()

    if existing_order:
        messages.warning(request, "Supply already added to cart.")
    else:
        SupplyOrder.objects.create(
            farmer=farmer,
            supply=supply,
            quantity=1,
            total_price=supply.price,
            status='Pending'
        )
        messages.success(request, "Supply added to cart successfully.")

    return redirect('cart_supply')



def cart_supply(request):
    farmer = Farmer.objects.get(user=request.user)
    cart_items = SupplyOrder.objects.filter(farmer=farmer, status='Pending')
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'farmer/cart_supply.html', {'cart_items': cart_items, 'total_price': total_price})

def increase_supply(request, order_id):
    order = get_object_or_404(SupplyOrder, id=order_id, farmer__user=request.user)
    available_stock = order.supply.quantity

    if order.quantity < available_stock:
        order.quantity += 1
        order.total_price = order.quantity * order.supply.price
        order.save()
    else:
        messages.warning(request, "Cannot increase quantity. Only {} items available in stock.".format(available_stock))

    return redirect('cart_supply')

def decrease_supply(request, order_id):
    order = get_object_or_404(SupplyOrder, id=order_id, farmer__user=request.user)
    if order.quantity > 1:
        order.quantity -= 1
        order.total_price = order.quantity * order.supply.price
        order.save()
    else:
        order.delete()
    return redirect('cart_supply')


def remove_supply(request, order_id):
    order = get_object_or_404(SupplyOrder, id=order_id, farmer__user=request.user)
    order.delete()
    return redirect('cart_supply')


def checkout_supply(request):
    farmer = get_object_or_404(Farmer, user=request.user)
    cart_items = SupplyOrder.objects.filter(farmer=farmer, status='Pending')
    total = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        method = request.POST.get('payment_method')

        holder = request.POST.get('card_holder')
        number = request.POST.get('card_number')
        expiry = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        delivery_name = request.POST.get('delivery_name')
        delivery_phone = request.POST.get('delivery_phone')
        delivery_address = request.POST.get('delivery_address')
        delivery_pin = request.POST.get('delivery_pin')

        if method == 'Card Payment':
            if not holder or not number or not expiry or not cvv:
                messages.warning(request, "All card details are required for card payment.")
                return redirect('checkout_supply')
            if len(number) != 16 or not number.isdigit():
                messages.warning(request, "Card number must be 16 digits.")
                return redirect('checkout_supply')
            if len(cvv) not in [3, 4] or not cvv.isdigit():
                messages.warning(request, "Invalid CVV.")
                return redirect('checkout_supply')

        if method == 'Home Delivery':
            if not delivery_name or not delivery_phone or not delivery_address or not delivery_pin:
                messages.warning(request, "Please fill in all delivery details.")
                return redirect('checkout_supply')

        status = 'Home Delivery' if method == 'Home Delivery' else 'Paid'

        checkout = SupplyCheckout.objects.create(
            farmer=farmer,
            payment_method=method,
            card_holder=holder if method == 'Card Payment' else None,
            card_number=number if method == 'Card Payment' else None,
            expiry_date=expiry if method == 'Card Payment' else None,
            cvv=cvv if method == 'Card Payment' else None,
            total_amount=total,
            status=status,
            delivery_name=delivery_name if method == 'Home Delivery' else None,
            delivery_phone=delivery_phone if method == 'Home Delivery' else None,
            delivery_address=delivery_address if method == 'Home Delivery' else None,
            delivery_pin=delivery_pin if method == 'Home Delivery' else None
        )

        for item in cart_items:
            SupplyCheckoutItem.objects.create(
                checkout=checkout,
                supply=item.supply,
                quantity=item.quantity
            )
            item.supply.quantity -= item.quantity
            item.supply.save()

        cart_items.delete()
        messages.success(request, "Order placed successfully!")
        return redirect('cart_supply')

    return render(request, 'farmer/checkout_supply.html', {'cart_items': cart_items, 'total': total})


def view_my_supply_orders(request):
    farmer = Farmer.objects.get(user=request.user)
    orders = SupplyCheckout.objects.filter(farmer=farmer).order_by('-id')
    return render(request, 'farmer/view_my_supply_orders.html', {'orders': orders})


def all_supply_orders_admin(request):
    orders = SupplyCheckout.objects.all().order_by('-id')
    deliveries = Delivery.objects.filter(user__is_active=True, user__usertype='Delivery')
    return render(request, 'admin/all_supply_orders_admin.html', {'orders': orders, 'deliveries': deliveries})




def assign_delivery_supply(request, order_id):
    if request.method == "POST":
        delivery_id = request.POST.get('delivery_id')
        order = get_object_or_404(SupplyCheckout, id=order_id)
        delivery = get_object_or_404(Delivery, id=delivery_id)
        order.assigned_delivery = delivery
        order.save()
        messages.success(request, f"Delivery person {delivery.name} assigned to order #{order.id}")
    return redirect('all_supply_orders_admin')




def delivery_assigned_supply_orders(request):
    delivery_user = request.user
    delivery = Delivery.objects.get(user=delivery_user)
    supply_orders = SupplyCheckout.objects.filter(assigned_delivery=delivery)
    return render(request, 'delivery/delivery_assigned_supply_orders.html', {'supply_orders': supply_orders})



def update_supply_delivery_status(request, checkout_id):
    if request.method == 'POST':
        status = request.POST.get('delivery_status')
        checkout = SupplyCheckout.objects.get(id=checkout_id)
        checkout.delivery_status = status
        checkout.save()
        messages.success(request, "Delivery status updated successfully.")
        return redirect('delivery_assigned_supply_orders')


def verify_supply_payment_status(request, checkout_id):
    if request.method == 'POST':
        status = request.POST.get('payment_verification')
        checkout = SupplyCheckout.objects.get(id=checkout_id)
        checkout.payment_verification = status
        checkout.save()
        messages.success(request, "Payment status updated successfully.")
        return redirect('delivery_assigned_supply_orders')

def submit_supply_review(request, checkout_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        checkout = SupplyCheckout.objects.get(id=checkout_id)
        farmer = Farmer.objects.get(user=request.user)

        SupplyReview.objects.create(
            checkout=checkout,
            farmer=farmer,
            rating=rating,
            comment=comment
        )

        messages.success(request, "Thank you for your feedback.")
        return redirect('view_my_supply_orders')


def view_my_supply_reviews(request):
    farmer = Farmer.objects.get(user=request.user)
    reviews = SupplyReview.objects.filter(farmer=farmer).order_by('-created_at')
    return render(request, 'farmer/view_my_supply_reviews.html', {'reviews': reviews})


def view_all_my_reviews(request):

    supply_reviews = SupplyReview.objects.all()
    product_reviews = Review.objects.all()

    return render(request, 'admin/view_all_my_reviews.html', {
        'supply_reviews': supply_reviews,
        'product_reviews': product_reviews,
    })


def delete_supply_review(request, review_id):
    farmer = Farmer.objects.get(user=request.user)
    review = get_object_or_404(SupplyReview, id=review_id, farmer=farmer)
    review.delete()
    messages.success(request, "Your review has been deleted.")
    return redirect('view_my_supply_reviews')


from django.contrib import messages
from .models import FavoriteSupply, Supply, Login, Farmer

def add_to_favorite_supply(request, supply_id):
    if 'uid' in request.session:
        login_id = request.session['uid']
        user = Farmer.objects.get(user__id=login_id)
        supply = get_object_or_404(Supply, id=supply_id)

        FavoriteSupply.objects.get_or_create(user=user, supply=supply)
        messages.success(request, "Supply added to favorites.")
    return redirect('view_favorites_supply')


def view_favorites_supply(request):
    if 'uid' in request.session:
        login_id = request.session['uid']
        user_obj = Farmer.objects.get(user__id=login_id)
        favorites = FavoriteSupply.objects.filter(user=user_obj)
        return render(request, 'farmer/view_favorites_supply.html', {'favorites': favorites})
    else:
        return redirect('logins')


def remove_favorite_supply(request, fav_id):
    FavoriteSupply.objects.filter(id=fav_id).delete()
    messages.success(request, "Favorite removed successfully.")
    return redirect('view_favorites_supply')




