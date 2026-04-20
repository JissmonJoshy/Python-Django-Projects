from django.shortcuts import render,redirect,get_object_or_404
from.models import*
from django.contrib import messages

def home(request):
    return render(request,"index.html")

def userhome(request):
    return render(request,"user/userhome.html")

def adminhome(request):
    return render(request,"Admin/adminhome.html")

def servicehome(request):
    return render(request,"service/index-3.html")

def servicereg(request):
    if request.method == "POST":  
        center_name = request.POST.get("center_name")
        service_type = request.POST.get("service_type")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")  
        email = request.POST.get("email")
        password = request.POST.get("password")
        image = request.FILES.get("image")  
        user = Login.objects.create(email=email, password=password, userType="Service")
        service = Services.objects.create(
            user=user,
            center_name=center_name,
            service_type=service_type,
            address=address,
            phone_number=phone_number,
            email=email,
            password=password,
            image=image,  
            )
        messages.success(request, "Registration successful")
        return redirect("/login/")

    return render(request, "serregister.html")

def ad(request):
    Login.objects.create(email="admin@gmail.com",password="admin123",userType="Admin")
    return redirect("/")


def customerreg(request):
    if request.method == "POST":  
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")  
        email = request.POST.get("email")
        password = request.POST.get("password")

        if Services.objects.filter(email=email).exists():
            messages.info(request, "Email already exists")
        else:
            user = Login.objects.create(email=email, password=password, userType='Customer')
            Customer.objects.create(
                user=user, name=name, address=address, phone_number=phone_number, email=email, password=password)
            messages.info(request, "Registration successful")
            return redirect('/login/') 

    return render(request, "custregister.html")


def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Login.objects.filter(email=email).first()
        
        if user:
            
                
                if user.userType == "Admin":
                    messages.success(request, "Login Successful ")
                    return redirect('/adminhome')

                elif user.userType == "Customer":
                    customer = Customer.objects.filter(user=user).first()
                    if customer:
                        # if customer.status == "approved":
                            request.session['uid'] = customer.user_id
                            messages.success(request, "Login Successful as Customer")
                            return redirect('/userhome')
                        # else:
                        #     messages.info(request, "Your account is pending approval.")
                    else:
                        messages.error(request, "Customer profile not found.")

                elif user.userType == "Service":
                    service = Services.objects.filter(user=user).first()
                    
                    if service:
                        if service.status == "Approved":
                            request.session['uid'] = service.user_id
                            messages.success(request, "Login Successful! Welcome back.")
                            return redirect('/servicehome')
                        
                        else:
                            messages.info(request, "Your account is pending approval.")
                    else:
                        messages.error(request, "Service profile not found.")

                    
                else:
                    messages.error(request, "Incorrect password.")

        else:
            messages.error(request, "Email not found.")

        return redirect('/login/')  
    return render(request, 'login.html')

# ADMIN


def service_center(request):
    ser = Services.objects.all()
    return render(request, 'Admin/service_center.html', {'ser': ser})

from django.shortcuts import render, redirect
from .models import Services, Login

def approve_center(request):
    service_id = request.GET.get("id")
    if service_id:
        service = Services.objects.filter(id=service_id).first()
        if service:
            service.status = "Approved"
            service.save()
    return redirect('/service_center/')

def reject_center(request):
    service_id = request.GET.get("id")
    if service_id:
        service = Services.objects.filter(id=service_id).first()
        if service:
            service.status = "Rejected"
            service.save()  # Update status to "Rejected"
    return redirect('/service_center/')

def delete_center(request):
    service_id = request.GET.get("id")
    if service_id:
        service = Services.objects.filter(id=service_id).first()
        if service:
            login_user = service.user  # Get the associated Login user
            service.delete()  # Delete from Services
            if login_user:
                login_user.delete()  # Delete the corresponding Login user
    return redirect('/service_center/')



def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'Admin/customer_list.html', {'customers': customers})

def approve_customer(request):
    customer_id = request.GET.get('id')
    customer = Customer.objects.get(id=customer_id)
    customer.status = "Approved"
    customer.save()
    return redirect('customer_list')

def reject_customer(request):
    customer_id = request.GET.get('id')
    customer = Customer.objects.get(id=customer_id)
    customer.status = "Rejected"
    customer.save()
    return redirect('customer_list')





#____________________________________           SERVICES        ______________________________________________#

def customer_approve(request):
    cus=Customer.objects.all()
    return render(request,"service/customerview.html",{'cus':cus})

def accept(request):
    id = request.GET.get("id")
    user = Customer.objects.filter(id=id).first()
    if user:
        user.status = "approved"
        user.save() 
        messages.info(request,'Approved successfully')
    return redirect('/customer_approve/')

def reject(request):
    id = request.GET.get("id")
    user = Customer.objects.filter(id=id).first()
    if user:
        user.status = "rejected" 
        user.save() 
    messages.info(request,'User will Rejected Success')
    return redirect('/customer_approve/')

def customer_rquest(request):
    uid = request.session.get("uid")  # Get logged-in service provider ID
    if not uid:
        messages.error(request, "You need to log in first.")
        return redirect('/login/')  # Redirect to login if not authenticated

    # Find the logged-in service provider
    service_provider = Services.objects.filter(user_id=uid).first()
    
    if service_provider:
        app = ServiceRequest.objects.filter(service=service_provider)  # Filter by service center
    else:
        app = []  # If service provider not found, return an empty list

    return render(request, "service/request_service.html", {'app': app})


def approveservice_request(request):
    id = request.GET.get("id")
    user = ServiceRequest.objects.filter(id=id).first()
    if user:
        user.status = "approved"
        user.save() 
        messages.info(request,'Approved successfully')
    return redirect('/customer_rquest/')

def delivery_list(request):
    agtm = DeliveryAgent.objects.all()
    return render(request,"service/agent.html",{'agtm':agtm})

def acceptagent(request):
    id = request.GET.get("id")
    user = DeliveryAgent.objects.filter(id=id).first()
    if user:
        user.status = "approved"
        user.save() 
        messages.info(request,'Approved successfully')
    return redirect('/delivery_list/')

def completeser(request):
    id = request.GET.get("id")
    user = ServiceRequest.objects.filter(id=id).first()
    if user:
        user.status = "Completed"
        user.save() 
        messages.info(request,'Approved successfully')
    return redirect('/customer_rquest/')

def rejectagent(request):
    id = request.GET.get("id")
    user = DeliveryAgent.objects.filter(id=id).first()
    if user:
        user.status = "rejected" 
        user.save() 
    messages.info(request,'User will Rejected Success')
    return redirect('/delivery_list/')

def sparelist_ser(request):
    spr = Spare.objects.all()
    return render(request,"service/sparelist.html",{'spr':spr})

def addcart(request):
    id =request.GET.get("id")
    uid = request.session.get("uid")
    user = Services.objects.get(id=uid)  
    product = Spare.objects.get(id=id)
   
    cart=CartItem.objects.create(user=user, product=product)
    return redirect('/sparelist_ser/',{'product':product})


def cartlist(request):
    uid = request.session.get("uid")
    view = CartItem.objects.filter(user=uid)
    cart = Spare.objects.all()
    total_amount = 0
    
    for item in view:
        item.total_amount = item.product.price * item.quantity
        total_amount += item.total_amount
    return render(request, "service/cart.html", {'view': view,'cart':cart,'total_amount':total_amount})

def deletecartid(request):
    id = request.GET.get('id')
    delete = CartItem.objects.filter(id=id).delete()
    print(delete)
    messages.info(request,"sucessfully Remove")
    return redirect('/cartlist')

def order(request):
    total_amount = request.GET.get('total_amount')
    uid = request.session.get("uid")
    user = Services.objects.get(id=uid)
    cart = CartItem.objects.filter(user=user)
    total = sum(i.product.price * i.quantity for i in cart)

    if request.POST:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')

        order_ids = []  

        for item in cart:
            order = Order.objects.create(
                product=item.product,
                user=user,
                name=name,
                phone=phone,
                address=address,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country
            )
            order_ids.append(order.id)

        cart.update(status="ordered")
        
        return redirect(f'/payment?order_id={order_ids[-1]}&total={total_amount}')

    return render(request, 'service/createorder.html', {'cart': cart, 'total_amount': total_amount})


def payment(request):
    order_id = request.GET.get('order_id') 
    total = request.GET.get('total')  
    print(total,"KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    uid = request.session.get('uid') 

    if order_id:
        try:
            order = Order.objects.get(id=order_id, user_id=uid)
            if not total:
                total = sum(item.product.price * item.quantity for item in order.items.all())
            if not total or float(total) <= 0:
                return render(request, "user/payment.html", {'total': total})

            if request.method == 'POST':
                order.payment_status = 'paid'
                order.save()

                cart_items = CartItem.objects.filter(user=order.user)
                cart_items.delete() 
                messages.success(request, 'Payment successfully')
                return redirect('/orderdetails')

        except Order.DoesNotExist:
            messages.error(request, 'Order not found or invalid order ID')
            return redirect('/orderdetails')
    else:
        messages.error(request, 'Payment successfully')
        return redirect('/orderdetails')
    return render(request, "service/payment.html", {'total': total})

def orderdetails(request):
    uid = request.session["uid"]
    total = request.GET.get('total') 
    det  = Order.objects.filter(id=uid)
    return render(request,"service/orderdetails.html",{'det':det,'total':total})


def add_amount(request):
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        amount = request.POST.get("amount")

        service_request = ServiceRequest.objects.get(id=request_id)
        service_request.amount = amount 
        service_request.save()
        return redirect("/customer_rquest/")  
       
# *********************************        CUSTOMER          **********************************#

def service_centerview(request):
    ser  = Services.objects.all()
    return render(request, 'user/service_center.html',{'ser':ser})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Services, ServiceRequest, Customer

def servicerequest(request):
    service_id = request.GET.get("id")  # Get service center ID from URL
    service = get_object_or_404(Services, id=service_id)  # Fetch service center
    uid = request.session.get("uid")  # Get logged-in user ID

    if not uid:
        messages.error(request, "You need to log in first.")
        return redirect("/login/")

    user = get_object_or_404(Customer, user=uid)  # Get logged-in customer

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        car_model = request.POST.get("car_model")
        license_plate = request.POST.get("license_plate")
        service_date = request.POST.get("service_date")
        service_time = request.POST.get("service_time")
        description = request.POST.get("description")

        ServiceRequest.objects.create(
            user=user,
            service=service,  # Save the service center
            name=name,
            phone=phone,
            car_model=car_model,
            license_plate=license_plate,
            service_date=service_date,
            service_time=service_time,
            description=description
        )

        messages.success(request, "Service request created successfully!")
        return redirect("/requestdetails/")  # Redirect to the service request details page

    return render(request, "user/requestform.html", {"service": service})

####################################################

def requestdetails(request):
    uid = request.session.get("uid")  # Use .get() to avoid errors if 'uid' is missing
    if not uid:
        messages.error(request, "You need to log in first.")
        return redirect('/login/')  # Redirect to login page if not logged in

    # Filter service requests for the logged-in customer
    customer = Customer.objects.filter(user_id=uid).first()
    if customer:
        det = ServiceRequest.objects.filter(user=customer)  # Filter by customer
    else:
        det = []  # If customer not found, return an empty list

    return render(request, "user/requestdetails.html", {'det': det})


def payment(request):
    request_id = request.GET.get("id")
    return render(request, "user/payment.html", {"request_id": request_id})

def update_payment(request):
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        ServiceRequest.objects.filter(id=request_id).update(status="Paid")
        messages.success(request, "Payment Successful!")
        return redirect("/requestdetails/")




def give_feedback(request, service_id):
    # Ensure user is logged in by checking session
    if 'uid' not in request.session:
        return redirect("/login")  # Redirect to login if not logged in

    # Get the logged-in customer from session
    try:
        customer = Customer.objects.get(user_id=request.session['uid'])
    except Customer.DoesNotExist:
        return redirect("/login")  # Redirect if customer does not exist

    service_request = ServiceRequest.objects.get(id=service_id)

    if request.method == "POST":
        title = request.POST.get("title")
        feedback_text = request.POST.get("feedback")

        if title and feedback_text:
            Feedback.objects.create(
                user=customer,  # Use customer object retrieved from session
                service_request=service_request,
                title=title,
                feedback=feedback_text
            )
            return redirect("/requestdetails")  # Redirect after feedback submission

    return render(request, "user/give_feedback.html", {"service_request": service_request})



def view_feedback(request):
    uid = request.session.get("uid")  # Get logged-in customer ID
    if not uid:
        messages.error(request, "You need to log in first.")
        return redirect('/login/')  

    # Find the logged-in customer
    customer = Customer.objects.filter(user_id=uid).first()
    
    if customer:
        feedbacks = Feedback.objects.filter(user=customer)  # Get only the logged-in user's feedbacks
    else:
        feedbacks = []

    return render(request, "user/view_feedback.html", {'feedbacks': feedbacks})



def delete_feedback(request, feedback_id):
    uid = request.session.get("uid")  # Get logged-in user ID
    if not uid:
        messages.error(request, "You need to log in first.")
        return redirect('/login/')  

    feedback = Feedback.objects.filter(id=feedback_id, user__user_id=uid).first()
    
    if feedback:
        feedback.delete()
        messages.success(request, "Feedback deleted successfully.")
    else:
        messages.error(request, "Feedback not found.")

    return redirect('/view_feedback/')



from django.shortcuts import render
from .models import Feedback, Services, ServiceRequest

def service_feedbacks(request):
    # Ensure user is logged in as a service provider
    if 'uid' not in request.session:
        return redirect("/login")

    # Get the logged-in service provider
    try:
        service = Services.objects.get(user_id=request.session['uid'])
    except Services.DoesNotExist:
        return redirect("/login")

    # Get all service requests related to this service provider
    service_requests = ServiceRequest.objects.filter(service=service)

    # Get feedback for those service requests
    feedbacks = Feedback.objects.filter(service_request__in=service_requests)

    return render(request, "service/service_feedbacks.html", {"feedbacks": feedbacks})

def admin_feedbacks(request):
    feedbacks = Feedback.objects.all()
    return render(request, "Admin/admin_feedbacks.html", {"feedbacks": feedbacks})





######################################################
def delete_data(request):
    id=request.GET.get('id')
    print(id)
    delete=ServiceRequest.objects.filter(id=id).delete()
    messages.info(request,"Deteted")
    return redirect('/requestdetails/')

def sell_vechile(request):
    uid = request.session["uid"]
    customer = request.POST.get("id")
    customer = Customer.objects.get(id=uid)
    print(customer,"_________________________________________________________________________________")
    service = Services.objects.get(id=uid)
    print(service,"****************************************************")
    if request.POST:
        vehiclename = request.POST["vehiclename"]
        make_year = request.POST["make_year"]
        price = request.POST["price"]
        description = request.POST["description"]
        image = request.FILES['image']

        vc=Vehicle.objects.create(
            service=service,
            customer=customer,
            vehiclename=vehiclename,
            make_year=make_year,
            price=price,
            description=description,
            image=image
        )
        messages.success(request, "Vehicle added for sale successfully!")
        return redirect('/userhome/')

    return render(request, 'user/sell_vehicle.html')

def vechile_list(request):
    uid = request.session.get('uid')
    list = Vehicle.objects.filter(id=uid)
    return render(request,"user/shop.html",{'list':list})


def userfeedback(request):
    id = request.GET.get("id")  
    uid = request.session["uid"]
    user = Customer.objects.get(id=uid)
    print(user,"............................................")   
    if request.POST:
        feedback = request.POST.get('feedback')
        abc = Feedback.objects.create(user=user,feedback=feedback)
        abc.save()
        return redirect('/userhome')
    return render(request,"user/userfeedback.html")

def vechile_buylist(request):
     uid = request.session.get('uid')
     lis = Vehicle.objects.filter(id = uid)
     return render(request,"user/vechilelist.html",{'lis':lis})

def approve_vechile(request):
    id = request.GET.get("id")
    user = Vehicle.objects.filter(id=id).first()
    if user:
        user.status = "Approved"
        user.save() 
        messages.info(request,'Approved successfully')
    return redirect('/vechile_buylist/')

def vehicle_rejectq(request):
    id = request.GET.get("id")
    user = Vehicle.objects.filter(id=id).first()
    if user:
        user.status = "Rejected"
        user.save() 
        messages.info(request,'Rejected successfully')
    return redirect('/vechile_buylist/')

# +++++++++++++++++++++++++++++++++++++++++++ DELIVERY AGENT ++++++++++++++++++++++++++++++++++++++++++

def deliverypick(request):
    pice = ServiceRequest.objects.all()
    return render(request,"delivery/request.html",{'pice':pice})


def approvedel_request(request):
    id = request.GET.get("id")
    user = ServiceRequest.objects.filter(id=id).first()
    if user:
        user.status = "Delivered"
        user.save() 
        messages.info(request,'Delivery successfully')
    return redirect('/deliverypick/')

def approvedel(request):
    id = request.GET.get("id")
    user = ServiceRequest.objects.filter(id=id).first()
    if user:
        user.status = "Approved"
        user.save() 
        messages.info(request,'Approved successfully')
    return redirect('/deliverypick/')


def rejectdel_request(request):
    id = request.GET.get("id")
    user = ServiceRequest.objects.filter(id=id).first()
    if user:
        user.status = "rejected" 
        user.save() 
    messages.info(request,'User will Rejected Success')
    return redirect('/deliverypick/')


# ********************** Exporter ***********************************

def add_spare(request):
    uid = request.session["uid"]
    user = request.POST.get("id")
    user = Exporter.objects.get(id=uid)
    if request.method == 'POST':
        name = request.POST.get('name')
        part_number = request.POST.get('part_number')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
 
        spare = Spare.objects.create(
            user=user,
            name=name,
            part_number=part_number,
            description=description,
            price=price,
            image=image
        )
        return redirect('/sparelist/')
    return render(request, 'exporter/addspare.html')

def sparelist(request):
    spr = Spare.objects.all()
    return render(request,"exporter/sparelist.html",{'spr':spr})

def exp_detail(request):
     uid = request.session.get('uid')
     ord = Order.objects.all()
     return render(request,"exporter/orderdetail.html",{'ord':ord})

def shipped(request):
    id = request.GET.get("id")
    order = Order.objects.filter(id=id).first()
    if order:
        order.status = "Shipped"
        order.save() 
        messages.info(request,'Shipped successfully')
    return redirect('/exp_detail')

def delivered(request):
    id = request.GET.get("id")
    order = Order.objects.filter(id=id).first()
    if order:
        order.status = "delivered"
        order.save() 
        messages.info(request,'delivered successfully')
    return redirect('/exp_detail')

def deletebb(request):
    id = request.GET.get('id')
    delete = Order.objects.filter(id=id).delete()
    messages.info(request,"sucessfully Remove")
    return redirect('/exp_detail')

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


from datetime import date as date, datetime as dt
from django.db.models import Q, Min, Max

def chat(request):
    uid = request.session["uid"]
    sellerid = request.GET.get('id')  #
    print(sellerid,"%%%%%%")
    name = ""
    artistData = Customer.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(sellerid__user=uid) & Q(customerid=id))
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    user = Services.objects.get(user=uid)
    print(user,"**************")
    if id:
        customerid = Customer.objects.get(id=id)
        name = customerid.name 
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            sellerid=user, message=message, customerid=customerid, time=formatted_time, utype="service")
        sendMsg.save()
    return render(request, "service/reciever.html", {"artistData": artistData, "getChatData": getChatData, "customerid": name, "id": id})


def reply(request):
    uid = request.session["uid"]
    name = ""
    userData = Services.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(customerid__user=uid) & Q(sellerid=id))
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    customerid = Customer.objects.get(user=uid)
    if id:
        userid = Services.objects.get(id=id)
        name = userid.center_name
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            sellerid=userid, message=message, customerid=customerid, time=formatted_time, utype="CUSTOMER")
        sendMsg.save()
    return render(request, "user/sender.html", {"userData": userData, "getChatData": getChatData, "userid": name, "id": id})

def billview(request):
    cus = Customer.objects.all()
    ser = ServiceRequest.objects.all()
    ord  = Order.objects.all()
    return render(request,"bill.html",{'cus':cus,'ser':ser,'ord':ord})



def dlt(request):
      # List of IDs to delete
    Login.objects.filter(id='1').delete()
    return redirect('/')