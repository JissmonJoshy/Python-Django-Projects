from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserReg(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    contact = models.CharField(max_length = 20)
    email = models.EmailField()
    address = models.CharField(max_length = 50)
    health = models.CharField(max_length = 500,null= True)#Health status
    user = models.ForeignKey(User,on_delete=models.CASCADE,null = True)

class LabReg(models.Model):
    name = models.CharField(max_length = 20)
    location = models.CharField(max_length = 20)
    contact = models.CharField(max_length = 20)
    email = models.EmailField()
    address = models.CharField(max_length = 50)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null = True)

class Tests(models.Model):
    lab = models.ForeignKey(LabReg, on_delete=models.CASCADE)
    test = models.CharField(max_length = 50)
    description = models.CharField(max_length = 50)
    price = models.IntegerField()

class Slots(models.Model):
    lab = models.ForeignKey(LabReg,on_delete = models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(UserReg,on_delete = models.CASCADE,null = True)
    test = models.ForeignKey(Tests,on_delete = models.CASCADE,null = True)
    report = models.FileField(null = True)
    prescription = models.CharField(max_length = 200,null = True)
    testStatus = models.IntegerField(default=0)

class Payment(models.Model):
    date = models.DateField(auto_now_add = True)
    time = models.TimeField(auto_now = True)
    amount = models.DecimalField(decimal_places = 2,max_digits = 6)
    user = models.ForeignKey(UserReg,on_delete = models.CASCADE)
    slot = models.ForeignKey(Slots,on_delete = models.CASCADE)
    status = models.CharField(max_length=20,default="Succesfull")

