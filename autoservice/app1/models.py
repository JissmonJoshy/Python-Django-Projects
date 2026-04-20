from django.db import models
from datetime import datetime

class Login(models.Model):
    email = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    userType = models.CharField(max_length=100, null=True)

class Customer(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=100, null=True, default="pending")

class Services(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE,null=True)
    center_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    image = models.ImageField(upload_to='spare_parts/', blank=True, null=True)
    status = models.CharField(max_length=100, null=True, default="pending")


# class Exporter(models.Model):
#     user = models.ForeignKey(Login, on_delete=models.CASCADE,null=True)
#     firstname = models.CharField(max_length=100)
#     lastname = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=15)
#     email = models.EmailField()
#     password = models.CharField(max_length=128)
#     address = models.CharField(max_length=100)

class ServiceRequest(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE,null=True)   
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    car_model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    service_date = models.DateField()
    service_time = models.TimeField()
    description = models.TextField()
    amount = models.CharField(max_length=50,null=True)
    status = models.CharField(max_length=20,default='pending')
    payment_status = models.CharField(max_length=20,default='pending')

class Feedback(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, null=True)  # Connect to ServiceRequest
    title = models.CharField(max_length=100, null=True)
    feedback = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    sellerid = models.ForeignKey(Services, on_delete=models.CASCADE)
    customerid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    time = models.CharField(max_length=100)
    utype = models.CharField(max_length=100)
