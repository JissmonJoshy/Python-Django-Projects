from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from datetime import date as date, datetime as dt
from django.db.models import Q, Min, Max


def adm(request):
    adm=Login.objects.create_superuser(username='admin',email='admin@gmail.com',view_password='admin',password='admin',usertype='admin')
    adm.save()
    return redirect('/')


# Create your views here.
def index(request):
    return render(request,'index.html')

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active: 
                auth_login(request, user)  
                
                if user.usertype == 'admin':
                    messages.info(request, 'Welcome to admin page')
                    return redirect('/adminHome')
                elif user.usertype == "User":
                    request.session['uid'] = user.id
                    messages.info(request, "Welcome to User Page")
                    return redirect('/userHome')
                elif user.usertype == "contractor":
                    request.session['uid'] = user.id
                    messages.info(request, "Welcome to Contractor Page")
                    return redirect('/consHome')
                elif user.usertype == "worker":
                    request.session['uid'] = user.id
                    messages.info(request, "Welcome to Worker Page")
                    return redirect('/workerHome')
                else:
                    messages.error(request, "Invalid user type.")
                    return redirect('/')
            else:
                messages.error(request, "Your account is inactive. Please contact support.")
                return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('/')

    return render(request, 'login.html')




#Register
import re


def userRegister(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        place = request.POST['place']
        image = request.FILES.get("image")
        password = request.POST['password']

        # Email validation - must contain '@' and end with '.com'
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com)$"
        if not re.match(email_pattern, email):
            messages.error(request, "Invalid email. Email must contain '@' and end with '.com'.")
            return redirect('/userRegister')

        # Creating user if email is valid
        log = Login.objects.create_user(
            username=email,
            password=password,
            view_password=password,
            is_active=1,
            usertype='User'
        )
        log.save()

        reg = User.objects.create(
            loginId=log,
            name=name,
            email=email,
            phone=phone,
            image=image,
            place=place,
        )
        reg.save()

        messages.success(request, "Registration Successful")
        return redirect('/login')

    return render(request, 'register.html')



def ConRegister(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        place = request.POST['place']
        image = request.FILES["image"]
        password = request.POST['password']
        
        # Email validation - must contain '@' and end with '.com'
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com)$"
        if not re.match(email_pattern, email):
            messages.error(request, "Invalid email. Email must contain '@' and end with '.com'.")
            return redirect('/ConRegister')

        log = Login.objects.create_user(
            username=email,
            password=password,
            view_password=password,
            is_active=0,
            usertype='contractor')
        log.save()
        reg = Contractor.objects.create(
            loginId=log,
            name=name,
            email=email,
            phone=phone,
            image=image,
            place=place,)
        reg.save()
        messages.success(request, "Registration Successful ")
        return redirect('/login')
    return render(request,'register.html')



def WorkerRegister(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        place = request.POST['place']
        image = request.FILES["image"]
        job_type= request.POST['job_type']
        password = request.POST['password']
        experience= request.POST['experience']
 


        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com)$"
        if not re.match(email_pattern, email):
            messages.error(request, "Invalid email. Email must contain '@' and end with '.com'.")
            return redirect('/WorkerRegister')
        

        log = Login.objects.create_user(
            username=email,
            password=password,
            view_password=password,
            is_active=0,
            usertype='worker')
        log.save()
        reg = Worker.objects.create(
            loginId=log,
            name=name,
            email=email,
            phone=phone,
            image=image,
            job_type=job_type,
            experience=experience,
            place=place,)
        reg.save()
        messages.success(request, "Registration Successful ")
        return redirect('/login')
    return render(request,'WORKER/workerRegister.html')



#admin
# def admin(request):
#     adm=Login.objects.create_user(username='admin',view_password='admin',password='admin',usertype="admin")
#     adm.save()
#     return redirect('/')

def adminHome(request):
    return render(request,'ADMIN/adminHome.html')


def adminView_user(request):
    data=User.objects.all()
    return render(request,'ADMIN/adminView_user.html',{'data':data})


def adminConView(request):
    data=Contractor.objects.all()
    return render(request,'ADMIN/adminConView.html',{'data':data})

def adminWorker(request):
    data=Worker.objects.all()
    return render(request,'ADMIN/adminWorker.html',{'data':data})


def adminViewRequest(request):
    data = Request.objects.all().order_by('-id')
    return render(request, 'ADMIN/adminViewRequest.html', {'data': data})

def  deleteUser(request):
    id = request.GET.get('id')
    User.objects.filter(loginId__id=id).delete()
    Login.objects.filter(id=id).delete()
    messages.success(request, "user deleted")
    return redirect('/adminView_user')

def deleteWorkers(request):
    id = request.GET.get('id')
    Worker.objects.filter(loginId__id=id).delete()
    Login.objects.filter(id=id).delete()
    messages.success(request, "Worker deleted")
    return redirect('/adminWorker')

def ApproveCon(request):
    id = request.GET.get('id')
    Contractor.objects.filter(loginId__id=id).update(status="APPROVE")
    Login.objects.filter(id=id).update(is_active=1)
    messages.success(request, "Contractor has been Assigned")
    return redirect('/adminConView')


def dltCon(request):
    id = request.GET.get('id')
    Worker.objects.filter(loginId__id=id).delete()
    Login.objects.filter(id=id).delete()
    messages.success(request, "Contractor deleted")
    return redirect('/adminConView')




#user
def userHome(request):
    return render(request,'USER/userHome.html')


def viewUserprofile(request):
    uid=request.session['uid']
    data=User.objects.filter(loginId=uid)
    return render(request,'USER/viewUserprofile.html',{'data':data})

# def request_form(request):
#     if request.method == "POST":
#         user_id = request.session.get('uid')  
#         user = User.objects.get(loginId=user_id)  
#         contractor_id = request.POST['contractor']  
#         start_date = request.POST['start_date']
#         end_date = request.POST['end_date']
#         plot=request.POST['plot']
#         try:
#             start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
#             end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
#         except ValueError:
#             messages.error(request, "Invalid date format")
#             return redirect('/userHome')  
#         today = timezone.now().date()
#         if start_date_obj < today:
#             messages.error(request, "You cannot request work for a past date.")
#             return redirect('/userHome')
#         if end_date_obj < start_date_obj:
#             messages.error(request, "End date cannot be earlier than start date.")
#             return redirect('/userHome')
#         try:
#             contractor = Contractor.objects.get(id=contractor_id)
#             if Request.objects.filter(contractor=contractor, start_date=start_date_obj, end_date=end_date_obj,plot=plot).exists():
#                 messages.error(request, "This contractor is already booked for the selected date range.")
#                 return redirect('/userHome')
#             request_obj = Request(user=user, contractor=contractor, start_date=start_date_obj,plot=plot, end_date=end_date_obj)
#             request_obj.save()
#             messages.success(request, "Your request has been successfully submitted!")
#             return redirect('/userHome')  
#         except Contractor.DoesNotExist:
#             messages.error(request, "Invalid contractor selected.")
#             return redirect('/userHome')
        
           
#     else:
#         contractors = Contractor.objects.all()   
#         return render(request, 'user/request_form.html', {'contractors': contractors})




def request_form(request):
    if request.method == "POST":
        user_id = request.session.get('uid')
        user = User.objects.get(loginId=user_id)
        contractor_id = request.POST['contractor']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        plot = request.POST['plot']
        category = request.POST['category']
        
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format")
            return redirect('/userHome')
        
        today = timezone.now().date()
        if start_date_obj < today:
            messages.error(request, "You cannot request work for a past date.")
            return redirect('/userHome')
        
        if end_date_obj < start_date_obj:
            messages.error(request, "End date cannot be earlier than start date.")
            return redirect('/userHome')

        try:
            contractor = Contractor.objects.get(id=contractor_id)
            
            
            if Request.objects.filter(contractor=contractor, start_date=start_date_obj, end_date=end_date_obj, plot=plot).exists():
                messages.error(request, "This contractor is already booked for the selected date range.")
                return redirect('/userHome')

         
            request_obj = Request(user=user, contractor=contractor, start_date=start_date_obj, plot=plot, end_date=end_date_obj, category=category)
            request_obj.save()

           
            messages.success(request, "Your request has been successfully submitted!")
            return redirect('/userHome')

        except Contractor.DoesNotExist:
            messages.error(request, "Invalid contractor selected.")
            return redirect('/userHome')
    
    else:
        contractors = Contractor.objects.filter(status="APPROVE")
        return render(request, 'user/request_form.html', {'contractors': contractors})



def viewWorkers(request):
    data=Worker.objects.filter(Q(status="AVAILABLE") | Q(status="ASSIGNED"))
    return render(request,'USER/viewWorkers.html',{'data':data})


def userReq(request):
    uid = request.session['uid']
    user = User.objects.get(loginId=uid)

    # optimize queries (important)
    data = Request.objects.filter(user=user).prefetch_related(
        'assignedworker_set__worker',
        'assignedworker_set__workimage_set'
    )

    return render(request, 'USER/userReq.html', {'data': data})


# def useraddfeedback(request):
#     uid=request.session['uid']
#     id=request.GET.get('id')
#     user=User.objects.get(loginId=uid)
#     worker=Worker.objects.get(id=id)
#     if request.POST:
#         feedback=request.POST['feedback']
#         rating=request.POST['rating']
#         feedback=Feedback.objects.create(user=user,worker=worker,rating=rating,feedback=feedback,usertype="User")
#         feedback.save()
#         return redirect('/userHome')
#     return render(request,'USER/useraddfeedback.html')

def viewUserfeedback(request):
    uid=request.session['uid']
    user=User.objects.get(loginId=uid)
    data=Feedback.objects.filter(user=user,usertype="Worker")
    return render(request,'USER/viewUserfeedback.html',{'data':data})

def updateUser(request):
    uid = request.session.get('uid')
    data = User.objects.filter(loginId=uid)

    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        place = request.POST['place']
        if 'image' in request.FILES:
            image = request.FILES['image']
            data = Worker.objects.get(loginId=uid)
            data.name = name
            data.phone = phone
            data.place = place
            data.image = image
            data.save()
        else:
            User.objects.filter(loginId=uid).update(
                name=name,
                phone=phone,
                place=place
            )
        messages.success(request, 'Profile updated successfully')
        return redirect('/viewUserprofile')
    return render(request,'USER/updateUser.html',{'data':data})




def payment(request):
    id=request.GET.get('id')
    uid=request.session['uid']
    user=User.objects.filter(user_id=uid)
    product=Request.objects.filter(id=id)
    return render(request, 'USER/Payment.html')

  

def user_payment(request):
    id = request.GET.get('id') 
    req = Request.objects.get(id=id)
    amount = req.amount

    if request.method == 'POST':
        req.user_to_contractor_payment = "PAID"
        
        req.save()

        messages.success(request, "Payment successful!")
        return redirect('/userReq')  # Redirect after POST

    return render(request, "USER/user_payment.html", {
        'amount': amount
    })


def request_worker_change(request):
    req_id = request.GET.get('req_id')
    req = Request.objects.get(id=req_id)

    # ✅ جلوگیری duplicate request
    if req.worker_change_requested:
        messages.warning(request, "You have already requested a worker change. Please wait for contractor approval.")
        return redirect('/userHome')

    assigned = AssignedWorker.objects.get(request=req)
    current_worker = assigned.worker

    workers = Worker.objects.filter(
        job_type=current_worker.job_type,
        loginId__is_active=1,
        status__in=["AVAILABLE"]   # 🔥 only free workers (better)
    ).exclude(id=current_worker.id)

    if request.method == "POST":
        reason = request.POST.get('reason')
        new_worker_id = request.POST.get('worker')

        if not new_worker_id:
            messages.error(request, "Please select a worker")
            return redirect(request.path + f"?req_id={req_id}")

        new_worker = Worker.objects.get(id=new_worker_id)

        req.worker_change_requested = True
        req.worker_change_reason = reason
        req.requested_worker = new_worker
        req.save()

        messages.success(request, "Change request sent to contractor")
        return redirect('/userHome')

    return render(request, 'user/request_worker_change.html', {
        'request': req,
        'workers': workers
    })
def view_assigned_workers(request):
    uid = request.session.get('uid')
    user = User.objects.get(loginId=uid)

    data = AssignedWorker.objects.filter(user=user, status="ASSIGNED")

    return render(request, 'User/view_assigned_workers.html', {'data': data})


def user_view_con(request):
    data=Contractor.objects.filter(status='APPROVE')
    return render(request,'User/user_view_con.html',{'data':data})

#Contractor

def consHome(request):
    return render(request,'CONTRACTOR/consHome.html')


def viewConsprofile(request):
    uid=request.session['uid']
    data=Contractor.objects.filter(loginId=uid)
    return render(request,'CONTRACTOR/viewConsprofile.html',{'data':data})


def viewRequest(request):
    uid=request.session['uid']
    cont=Contractor.objects.get(loginId=uid)
    data=Request.objects.filter(contractor=cont)
    return render(request,'CONTRACTOR/viewRequest.html',{'data':data})


def viewWorker(request):
    pendingworker = Worker.objects.filter(status="PENDING")
    assignworker=Worker.objects.filter(Q(status="AVAILABLE") | Q(status="ASSIGNED"))

    
    data = {"assignworker": assignworker,
            "pendingworker": pendingworker}
    return render(request,'CONTRACTOR/viewWorker.html',data)

def ApproveWorker(request):
    id = request.GET.get('id')
    Worker.objects.filter(loginId__id=id).update(status="AVAILABLE")
    Login.objects.filter(id=id).update(is_active=1)
    messages.success(request, "Worker has been Assigned")
    return redirect('/viewWorker')

def deleteWorker(request):
    id = request.GET.get('id')
    Worker.objects.filter(loginId__id=id).delete()
    Login.objects.filter(id=id).delete()
    messages.success(request, "Worker deleted")
    return redirect('/viewWorker')

def deleteRequest(request):
    id=request.GET['id']
    Request.objects.filter(id=id).delete()
    return redirect('/viewRequest')

def updateContractor(request):
    uid = request.session.get('uid')
    data = Contractor.objects.filter(loginId=uid)

    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        place = request.POST['place']
        if 'image' in request.FILES:
            image = request.FILES['image']
            data = Contractor.objects.get(loginId=uid)
            data.name = name
            data.phone = phone
            data.place = place
            data.image = image
            data.save()
        else:
            Contractor.objects.filter(loginId=uid).update(
                name=name,
                phone=phone,
                place=place
            )
        messages.success(request, 'Profile updated successfully')
        return redirect('/viewConsprofile')
    return render(request,'Contractor/updateContractor.html',{'data':data})



def user_paid(request):
    uid = request.session['uid']
    cont = Contractor.objects.get(loginId=uid)
    con = AssignedWorker.objects.filter(contractor=cont).order_by('-id')

    return render(request, 'CONTRACTOR/user_paid.html', {'con': con})

def payWorker(request):
    worker_assignment_id = request.GET.get('id')  # Get ID from URL

    print("Worker Assignment ID from GET:", worker_assignment_id)  # Debugging

    if request.method == "POST":
        worker_assignment_id = request.POST.get("id")  # Get ID from form
        worker_amt = request.POST.get("workeramt")

        print("Worker Assignment ID from POST:", worker_assignment_id)  # Debugging
        print("Worker Amount:", worker_amt)  # Debugging

        if not worker_assignment_id or not worker_amt:
            messages.error(request, "Invalid payment request.")
            return redirect(request.path)

        try:
            worker_amt = float(worker_amt)
        except ValueError:
            messages.error(request, "Invalid amount entered.")
            return redirect(request.path)

        AssignedWorker.objects.filter(id=worker_assignment_id).update(
            contractor_status="PAID",
            payment_status="PAID",
            workeramt=worker_amt
        )

        messages.success(request, "Payment successful!")
        return redirect("/consHome")

    workers = AssignedWorker.objects.filter(contractor_status="PENDING")
    return render(request, 'CONTRACTOR/payWorker.html', {"workers": workers, "worker_id": worker_assignment_id})


def AssignWorker(request):
    req_id = request.GET.get('id')

    if not req_id:
        messages.error(request, "Request ID is missing.")
        return redirect('/viewRequest')

    req = Request.objects.get(id=req_id)

    # only available workers (optional improvement)
    workers = Worker.objects.filter(status__in=["AVAILABLE", "ASSIGNED"])

    if request.method == "POST":
        worker_ids = request.POST.getlist('worker')
        amount = request.POST.get('amount')

        if not worker_ids:
            messages.error(request, "Please select at least one worker.")
            return render(request, 'CONTRACTOR/AssignWorker.html', {'request': req, 'workers': workers})

        if not amount.isdigit():
            messages.error(request, "Enter valid amount.")
            return render(request, 'CONTRACTOR/AssignWorker.html', {'request': req, 'workers': workers})

        try:
            # update request
            req.amount = amount
            req.status = "ASSIGNED"
            req.save()

            for wid in worker_ids:
                worker = Worker.objects.get(id=wid)

                # create multiple entries
                AssignedWorker.objects.create(
                    contractor=req.contractor,
                    user=req.user,
                    request=req,
                    worker=worker,
                    status="ASSIGNED",
                    contractor_status="ASSIGNED",
                    payment_status="PENDING",
                    workeramt=amount
                )

                # update worker status
                worker.status = "ASSIGNED"
                worker.save()

            messages.success(request, "Workers assigned successfully!")
            return redirect('/viewRequest')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, 'CONTRACTOR/AssignWorker.html', {
        'request': req,
        'workers': workers
    })

def view_worker_change_requests(request):
    contractor = Contractor.objects.get(loginId=request.session.get('uid'))

    change_requests = Request.objects.filter(
        contractor=contractor,
        worker_change_requested=True
    )

    return render(request, 'contractor/view_worker_change_requests.html', {
        'change_requests': change_requests
    })


from django.core.exceptions import ObjectDoesNotExist

def assign_new_worker(request):
    req_id = request.GET.get('req_id')
    req = Request.objects.get(id=req_id)

    available_workers = Worker.objects.filter(status="AVAILABLE").exclude(id=req.worker.id)

    if request.method == "POST":
        new_worker_id = request.POST.get("worker")
        new_worker = Worker.objects.get(id=new_worker_id)

        if req.worker:
            req.worker.status = "AVAILABLE"  # Mark old worker as available
            req.worker.save()

        # Update Request model
        req.worker = new_worker
        req.worker.status = "ASSIGNED"
        req.worker_change_requested = False  
        req.worker_change_reason = None  
        req.save()

        try:
            assigned_worker = AssignedWorker.objects.get(request=req)
            assigned_worker.worker = new_worker
            assigned_worker.status = "ASSIGNED"
            assigned_worker.save()
        except ObjectDoesNotExist:
            AssignedWorker.objects.create(
                contractor=req.contractor,
                user=req.user,
                request=req,
                worker=new_worker,
                status="ASSIGNED"
            )

        messages.success(request, "Worker has been successfully changed and updated in assignment.")
        return redirect('/view_worker_change_requests')

    return render(request, 'contractor/assign_new_worker.html', {'req': req, 'available_workers': available_workers})

from django.shortcuts import render
from .models import Feedback

def contractor_feedback_view(request):
    # contractor = request.user.contractor  # Assuming contractor is logged in
    user_to_worker_feedbacks = Feedback.objects.filter(usertype="User")
    worker_to_user_feedbacks = Feedback.objects.filter(usertype="Worker")

    return render(request, 'Contractor/contractor_feedback.html', {
        'user_to_worker_feedbacks': user_to_worker_feedbacks,
        'worker_to_user_feedbacks': worker_to_user_feedbacks,
    })


def CON_user_view(request):
    data=User.obje
    return render(request,'Contractor/CON_user_view.html')



#Worker

def workerHome(request):
    return render(request,'WORKER/workerHome.html')

def viewWorkerprofile(request):
    uid=request.session['uid']
    data=Worker.objects.filter(loginId=uid)
    return render(request,'WORKER/viewWorkerprofile.html',{'data':data})


def updateWorker(request):
    uid = request.session.get('uid')
    data = Worker.objects.filter(loginId=uid)

    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        place = request.POST['place']
        if 'image' in request.FILES:
            image = request.FILES['image']
            data = Worker.objects.get(loginId=uid)
            data.name = name
            data.phone = phone
            data.place = place
            data.image = image
            data.save()
        else:
            Worker.objects.filter(loginId=uid).update(
                name=name,
                phone=phone,
                place=place
            )
        messages.success(request, 'Profile updated successfully')
        return redirect('/viewWorkerprofile')
    return render(request,'WORKER/updateWorker.html',{'data':data})

def viewFeedback(request):
    uid=request.session['uid']
    worker=Worker.objects.get(loginId=uid)
    data=Feedback.objects.filter(worker=worker,usertype="User")
    return render(request,'WORKER/viewFeedback.html',{'data':data})


def workeraddfeedback(request):
    uid=request.session['uid']
    id=request.GET.get('id')
    worker=Worker.objects.get(loginId=uid)
    user=User.objects.get(id=id)
    if request.POST:
        feedback=request.POST['feedback']
        rating=request.POST['rating']
        feedback=Feedback.objects.create(user=user,worker=worker,rating=rating,feedback=feedback,usertype="Worker")
        feedback.save()
        return redirect('/workerHome')
    return render(request,'WORKER/workeraddfeedback.html')


def ViewWork(request):
    uid = request.session['uid']

    worker = Worker.objects.get(loginId=uid)

    data = AssignedWorker.objects.filter(worker=worker, status="ASSIGNED")

    return render(request, 'WORKER/ViewWork.html', {'data': data})



def ViewPayment(request):
    uid=request.session['uid']
    worker=Worker.objects.get(loginId=uid)
    data=AssignedWorker.objects.filter(worker=worker)
    return render(request,'WORKER/ViewPayment.html',{'data':data})






#-------------Chat------------------



# def dlt(request):
 
#     Chat.objects.filter(id=100).delete()
#     return redirect('/')

def dlt(request):
    ids_to_delete = [100, 101, 102,103, 104,105,106,107,108,109,110,111,112,113]  # Add as many IDs as you want
    Chat.objects.filter(id__in=ids_to_delete).delete()
    return redirect('/')


def feedbackDEl(request):
    id=request.GET['id']
    Feedback.objects.filter(id=id).delete()
    return redirect('/userHome')




def chat(request):
    uid = request.session["uid"]
    user = User.objects.get(loginId=uid)
    contractors = Contractor.objects.filter(loginId__is_active=1)
    
    # Add unread message count for each contractor
    for contractor in contractors:
        contractor.unread_count = Chat.objects.filter(
            sender=user, receiver=contractor, is_Read=1
        ).count()

    # Get the contractor using the id from GET parameters
    id = request.GET.get("id")
    contractor = None
    chat_logs = None

    if id:
        try:
            contractor = Contractor.objects.get(id=id)  # Make sure to query Contractor
        except Contractor.DoesNotExist:
            contractor = None
        
        if contractor:
            # Now get chat logs between the user and the contractor
            chat_logs = Chat.objects.filter(sender=user, receiver=contractor)

            Chat.objects.filter(sender=user, receiver=contractor, is_Read=1).update(is_Read=2)
        
            if request.POST:
                message = request.POST["message"]
                sendMsg = Chat.objects.create(
                    sender=user,
                    message=message,
                    receiver=contractor,
                    userType="USER",
                    is_Read=3
                )
                sendMsg.save()
                return redirect('/chat?id=' + str(id))
    
    context = {
        "contractors": contractors,
        "contractor": contractor,
        "id": id,
        "chat_logs": chat_logs,
    }

    return render(request, "USER/chat.html", context)



def reply(request):
    uid = request.session["uid"]
    contractor = Contractor.objects.get(loginId=uid)
    users = User.objects.filter(loginId__is_active=1)

   
    for user in users:
        user.unread_count = Chat.objects.filter(
            sender=user, receiver=contractor, is_Read=3
        ).count()

    id = request.GET.get("id")
    user = None
    chat_logs = None

    if id:
        user = User.objects.get(id=id)
        chat_logs = Chat.objects.filter(sender=user, receiver=contractor)

       
        Chat.objects.filter(sender=user, receiver=contractor, is_Read=3).update(is_Read=2)

        if request.POST:
            message = request.POST["message"]
            sendMsg = Chat.objects.create(
                sender=user, message=message, receiver=contractor, userType="CONTRACTOR",is_Read=1)
            sendMsg.save()
            return redirect('/reply?id=' + str(id))

    context = {
        "users": users,
        "user": user,
        "id": id,
        "chat_logs": chat_logs,
    }

    return render(request, "CONTRACTOR/chat.html", context)


def upload_work_images(request):
    aw_id = request.GET.get('id')
    aw = AssignedWorker.objects.get(id=aw_id)

    if request.method == "POST":
        images = request.FILES.getlist('images')

        if not images:
            messages.error(request, "Please select images")
            return redirect(f'/upload_work_images?id={aw_id}')

        for img in images:
            WorkImage.objects.create(
                assigned_worker=aw,
                image=img
            )

        messages.success(request, "Images uploaded successfully")
        return redirect('/user_paid')

    return render(request, 'CONTRACTOR/upload_work_images.html', {'aw': aw})

def view_work_images(request):
    aw_id = request.GET.get('id')
    images = WorkImage.objects.filter(assigned_worker_id=aw_id)

    return render(request, 'CONTRACTOR/view_work_images.html', {'images': images})


def worker_details(request, id):
    worker = Worker.objects.get(id=id)

    # Get feedbacks for this worker
    feedbacks = Feedback.objects.filter(worker=worker)

    # Get assigned work images
    assigned = AssignedWorker.objects.filter(worker=worker)
    work_images = WorkImage.objects.filter(assigned_worker__in=assigned)

    return render(request, 'USER/worker_details.html', {
        'worker': worker,
        'feedbacks': feedbacks,
        'work_images': work_images
    })

def contractor_details(request, id):
    contractor = Contractor.objects.get(id=id)

    user_id = request.session.get('uid')

    # ✅ FIX HERE
    user = User.objects.get(loginId=user_id)

    feedbacks = Feedback.objects.filter(
        contractor=contractor,
        user=user
    )

    requests = Request.objects.filter(
        contractor=contractor,
        user=user
    )

    assigned = AssignedWorker.objects.filter(
        request__in=requests
    )

    work_images = WorkImage.objects.filter(
        assigned_worker__in=assigned
    )

    return render(request, 'USER/contractor_details.html', {
        'contractor': contractor,
        'feedbacks': feedbacks,
        'work_images': work_images
    })


def user_add_contractor_feedback(request):
    uid = request.session['uid']
    req_id = request.GET.get('req_id')

    user = User.objects.get(loginId=uid)
    req = Request.objects.get(id=req_id)

    contractor = req.contractor

    if request.method == "POST":
        feedback = request.POST['feedback']
        rating = request.POST['rating']

        Feedback.objects.create(
            user=user,
            contractor=contractor,
            request=req,   # ✅ LINK TO REQUEST
            rating=rating,
            feedback=feedback,
            usertype="User"
        )

        return redirect('/userReq')

    return render(request, 'USER/user_add_contractor_feedback.html', {'req': req})


def useraddfeedback(request):
    uid = request.session['uid']
    worker_id = request.GET.get('id')
    req_id = request.GET.get('req_id')

    user = User.objects.get(loginId=uid)
    worker = Worker.objects.get(id=worker_id)
    req = Request.objects.get(id=req_id)

    if request.method == "POST":
        feedback = request.POST['feedback']
        rating = request.POST['rating']

        Feedback.objects.create(
            user=user,
            worker=worker,
            request=req,   # ✅ IMPORTANT FIX
            rating=rating,
            feedback=feedback,
            usertype="User"
        )

        return redirect('/userReq')

    return render(request, 'USER/useraddfeedback.html')


def handle_worker_change(request):
    req_id = request.GET.get('req_id')
    action = request.GET.get('action')

    req = Request.objects.get(id=req_id)
    assigned = AssignedWorker.objects.get(request=req)

    if action == "accept":
        new_worker = req.requested_worker

        assigned.worker = new_worker
        assigned.save()

        req.worker_change_requested = False
        req.requested_worker = None
        req.worker_change_reason = None
        req.save()

        messages.success(request, "Worker change approved")

    elif action == "reject":
        req.worker_change_requested = False
        req.requested_worker = None
        req.save()

        messages.info(request, "Worker change rejected")

    return redirect('/view_worker_change_requests')