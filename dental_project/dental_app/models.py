from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)

class Patient(models.Model):
    patient_id = models.ForeignKey(Login,on_delete=models.CASCADE)
    username = models.CharField(max_length=20,null=True)
    name = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=30,null=True)
    address = models.TextField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    image = models.ImageField(upload_to='Image',null=True)
    state = models.CharField(max_length=30, null=True)  # New Field
    district = models.CharField(max_length=30, null=True)  # New Field
    
    pincode = models.CharField(max_length=6, null=True)  # New Field


class Dentist(models.Model):
    dentist_id = models.ForeignKey(Login,on_delete=models.CASCADE)
    username = models.CharField(max_length=20,null=True)
    name = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=30,null=True)
    address = models.TextField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    image = models.ImageField(upload_to='Image',null=True)
    licence = models.FileField(upload_to='Licenses', null=True, blank=True)
    experience = models.FileField(upload_to='Experience',null=True)
    state = models.CharField(max_length=30, null=True)  # New Field
    district = models.CharField(max_length=30, null=True)  # New Field
    
    pincode = models.CharField(max_length=6, null=True)  # New Field

class Lab(models.Model):
    lab_id = models.ForeignKey(Login,on_delete=models.CASCADE)
    username = models.CharField(max_length=20,null=True)
    name = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=30,null=True)
    address = models.TextField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    image = models.ImageField(upload_to='Image',null=True)
    state = models.CharField(max_length=30, null=True)  # New Field
    district = models.CharField(max_length=30, null=True)  # New Field
    
    pincode = models.CharField(max_length=6, null=True)  # New Field

class TimeSchedule(models.Model):
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    day = models.CharField(max_length=20,null=True)  
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    schedule = models.ForeignKey(TimeSchedule, on_delete=models.CASCADE)
    assigned_lab = models.ForeignKey(Lab, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Scheduled', 'Scheduled')
    ], default='Pending')
    assigned_time = models.TimeField(null=True, blank=True)  

class LabOrder(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)  
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)  
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)  
    order_type = models.CharField(max_length=50, choices=[
        ('Crown', 'Crown'),
        ('Bridge', 'Bridge'),
        ('Denture', 'Denture'),
        ('Braces', 'Braces'),
        ('Retainer', 'Retainer'),
        ('Teeth Whitening', 'Teeth Whitening'),
        ('Implant', 'Implant'),
        ('Other', 'Other'),
    ])
    
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Reviewed', 'Reviewed'),
    ], default='Pending')
    
    assigned_date = models.DateTimeField(auto_now_add=True)  
    
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)



class LabOrderRequest(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=50, choices=[
        ('Crown', 'Crown'),
        ('Bridge', 'Bridge'),
        ('Denture', 'Denture'),
        ('Braces', 'Braces'),
        ('Retainer', 'Retainer'),
        ('Teeth Whitening', 'Teeth Whitening'),
        ('Implant', 'Implant'),
        ('Other', 'Other'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ], default='Pending')
    requested_date = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE,null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True)
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE,null=True)
    rating = models.IntegerField(null=True,choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)