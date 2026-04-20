from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Login(AbstractUser):
    usertype=models.CharField(max_length=50,null=True)
    view_password=models.CharField(max_length=50,null=True)

class Expert(models.Model):
    login_id = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True)
    email = models.EmailField()
    contact = models.CharField(max_length=50,null=True)
    experience  = models.CharField(max_length=50,null=True)
    expertise   = models.CharField(max_length=50,null=True)
    address = models.TextField()
    file = models.FileField(upload_to='file', null=True)
        
class Customer(models.Model):
    login_id = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True)
    email = models.EmailField(null=True)
    contact = models.CharField(max_length=50,null=True)
    address = models.TextField(null=True)
    file = models.FileField(upload_to='file', null=True)
    
class Service(models.Model):
    name = models.CharField(max_length=50,null=True)
    price = models.CharField(max_length=50,null=True)
    description = models.TextField(null=True)
    file = models.FileField(upload_to='file', null=True)
    category = models.CharField(max_length=50,null=True)



class Skin(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    skintone = models.CharField(max_length=50, choices=[ 
        ('very_fair', 'Very Fair'),
        ('fair', 'Fair'),
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('olive', 'Olive'),
        ('tan', 'Tan'),
        ('deep_tan', 'Deep Tan'),
        ('brown', 'Brown'),
        ('dark', 'Dark'),
        ('deep_dark', 'Deep Dark'), 
    ], null=True)
    skintone_image = models.ImageField(upload_to='skintone_images/', null=True, blank=True)


class Bookings(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateField(null=True, blank=True)  
    time_schedule = models.TimeField(null=True, blank=True)
    assigned_expert = models.ForeignKey(Expert, on_delete=models.SET_NULL, null=True, blank=True)
    


class Chat(models.Model):
    sellerid = models.ForeignKey(Expert, on_delete=models.CASCADE)
    customerid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    time = models.CharField(max_length=100)
    utype = models.CharField(max_length=100)