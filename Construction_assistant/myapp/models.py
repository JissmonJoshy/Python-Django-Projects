from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=50,null=True)
    view_password=models.CharField(max_length=50,null=True)

class User(models.Model):
    loginId=models.ForeignKey(Login,on_delete=models.CASCADE,)
    name=models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    place = models.CharField(max_length=100, null=True)
    image = models.FileField(upload_to='file', null=True)

class Contractor(models.Model):
    loginId=models.ForeignKey(Login,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    place = models.CharField(max_length=100, null=True)
    image = models.FileField(upload_to='file', null=True)
    status = models.CharField(max_length=100, null=True, default="PENDING")

class Worker(models.Model):
    loginId=models.ForeignKey(Login,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    place = models.CharField(max_length=100, null=True)
    job_type = models.CharField(max_length=100, null=True)
    experience = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, null=True, default="PENDING")
    image = models.FileField(upload_to='file', null=True)


class Request(models.Model):
    contractor=models.ForeignKey(Contractor,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    # worker=models.ForeignKey(Worker,on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=100, null=True, default="PENDING")
    start_date = models.DateField(null=True, blank=True) 
    end_date = models.DateField(null=True, blank=True)
    category=models.CharField(max_length=50,null=True)
    plot=models.CharField(max_length=50,null=True)
    amount = models.CharField(max_length=100, null=True) 
    user_to_contractor_payment = models.CharField(max_length=100, default="PENDING")  
    contractor_to_worker_payment = models.CharField(max_length=100, default="PENDING")  
    worker_change_requested = models.BooleanField(default=False)  
    worker_change_reason = models.TextField(null=True, blank=True) 
    requested_worker = models.ForeignKey(Worker, null=True, blank=True, on_delete=models.SET_NULL)


class AssignedWorker(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    request=models.ForeignKey(Request,on_delete=models.CASCADE,null=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, null=True, default="PENDING")
    contractor_status = models.CharField(max_length=100, null=True, default="PENDING")
    payment_status = models.CharField(max_length=100, null=True, default="PENDING")
    workeramt=models.CharField(max_length=100, null=True)

class WorkImage(models.Model):
    assigned_worker = models.ForeignKey(AssignedWorker, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='work_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    contractor=models.ForeignKey(Contractor,on_delete=models.CASCADE,null=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)  
    worker=models.ForeignKey(Worker,on_delete=models.CASCADE,null=True)
    feedback=models.CharField(max_length=30,null=True)
    rating = models.CharField(max_length=100, null=True)
    usertype=models.CharField(max_length=100, null=True, default="PENDING") 



# class Chat(models.Model):
#     sellerid = models.ForeignKey(User, on_delete=models.CASCADE)
#     customerid = models.ForeignKey(Contractor, on_delete=models.CASCADE)
#     message = models.CharField(max_length=300)
#     date = models.DateField(auto_now=True)
#     time = models.CharField(max_length=100)
#     utype = models.CharField(max_length=100)
#     is_Read = models.BooleanField(default=False)


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    userType = models.CharField(max_length=100,null=True)
    is_Read = models.CharField(max_length=100,default=False)


