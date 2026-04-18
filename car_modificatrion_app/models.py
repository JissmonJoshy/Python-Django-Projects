from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)

class User(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    profile_image = models.ImageField(upload_to='user/')

class Employee(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    profile_image = models.ImageField(upload_to='employee/')
    operation = models.CharField(max_length=100,null=True)

class Service(models.Model):
    service_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/')
    created_at = models.DateTimeField(auto_now_add=True)
    operation = models.CharField(max_length=100,null=True)

class ServiceBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    car_number = models.CharField(max_length=20)
    car_name = models.CharField(max_length=100)
    problem_description = models.TextField()
    car_image = models.ImageField(upload_to='car_images/')

    status = models.CharField(max_length=50, default='Pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    estimate_date = models.DateField(null=True, blank=True)
    progress = models.PositiveIntegerField(default=0)

class Part(models.Model):
    part_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='parts/')
    operation = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class PartBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default='Pending')
    booked_date = models.DateTimeField(auto_now_add=True)
    @property
    def total_price(self):
        return self.quantity * self.part.price
    

class EmployeePartBooking(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default='Pending')
    booked_date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.quantity * self.part.price
