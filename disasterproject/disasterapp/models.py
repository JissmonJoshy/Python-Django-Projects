import email
from email.headerregistry import Address
from email.policy import default
from unittest.util import _MAX_LENGTH
from colorama import Fore
from django.db import models

# Create your models here.


class Login(models.Model):
    uname = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    userType = models.CharField(max_length=100, null=True)


class SocialRegister(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    state = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)


class UserReg(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    state = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)


class AuthReg(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    state = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)


class DonationCommon(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    cardno = models.IntegerField(null=True)
    cvv = models.IntegerField(null=True)
    mm = models.IntegerField(null=True)
    yy = models.IntegerField(null=True)
    amount = models.IntegerField(null=True)


class DonationRegUsers(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    cardno = models.IntegerField(null=True)
    cvv = models.IntegerField(null=True)
    mm = models.IntegerField(null=True)
    yy = models.IntegerField(null=True)
    amount = models.IntegerField(null=True)
    uid= models.IntegerField(null=True)


class Messages(models.Model):
    subject=models.CharField(max_length=100, null=True)
    date=models.DateField(null=True, blank=True)
    reply=models.CharField(max_length=100, null=True,default='Awaiting Response')
    status= models.CharField(max_length=100, null=True,default='Pending')

class Claims(models.Model):
    uid= models.CharField(max_length=100, null=True)
    fname= models.CharField(max_length=100, null=True)
    lname=  models.CharField(max_length=100, null=True)
    email= models.EmailField(max_length=100, null=True)
    phone= models.IntegerField(null=True)
    state= models.CharField(max_length=100, null=True)
    district= models.CharField(max_length=100, null=True)
    damages= models.CharField(max_length=100, null=True)
    bankname= models.CharField(max_length=100, null=True)
    aadhaar= models.IntegerField(null=True)
    accno= models.IntegerField(null=True)
    ifsc= models.CharField(max_length=100, null=True)
    branch= models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    image= models.ImageField(max_length=100, null=True)
    status= models.CharField(max_length=100, null=True)
    samount= models.CharField(max_length=100, null=True,default='None')


class Disaster(models.Model):
    uid= models.CharField(max_length=100, null=True)
    disaster=models.CharField(max_length=100, null=True)
    location= models.CharField(max_length=100, null=True)
    state= models.CharField(max_length=100, null=True)
    district= models.CharField(max_length=100, null=True)
    date=models.DateField(null=True, blank=True)
    des= models.CharField(max_length=100, null=True)
    image= models.ImageField(max_length=100, null=True)
    status= models.CharField(max_length=100, null=True,default='Pending')


class OfficerReg(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    state = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)


class CampReg(models.Model):
    officerid= models.CharField(max_length=100, null=True)
    name=models.CharField(max_length=100, null=True)
    email=models.EmailField(max_length=100, null=True)
    phone= models.IntegerField(null=True)
    date=models.DateField(null=True, blank=True)
    members=models.IntegerField(null=True)
    state= models.CharField(max_length=100, null=True)
    district=models.CharField(max_length=100, null=True)
    address=models.CharField(max_length=100, null=True)
    status=models.CharField(max_length=100,default='pending')


class CampMember(models.Model):
    campid = models.ForeignKey(CampReg, on_delete=models.CASCADE, null=True)
    name= models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone= models.IntegerField(null=True)
    age= models.IntegerField(null=True)
    state= models.CharField(max_length=100, null=True)
    district= models.CharField(max_length=100, null=True)
    address= models.CharField(max_length=100, null=True)


class CampRequirements(models.Model):
    campid = models.ForeignKey(CampReg, on_delete=models.CASCADE, null=True)
    officerid= models.CharField(max_length=100, null=True)
    name= models.CharField(max_length=100, null=True)
    quantity= models.IntegerField(null=True)
    remarks= models.CharField(max_length=100, null=True)
    date= models.DateField(null=True, blank=True)
    status= models.CharField(max_length=100, null=True,default='Requested')



class Complaint(models.Model):
    uid = models.ForeignKey(UserReg, on_delete=models.CASCADE, null=True)
    issue= models.CharField(max_length=100, null=True)
    description= models.CharField(max_length=100, null=True)
    date= models.DateField(max_length=100, null=True)
    status= models.CharField(max_length=100, null=True,default='raised')
    reply= models.CharField(max_length=100, null=True,default='No Reply')


class UserDonation(models.Model):
    uid=models.IntegerField(null=True)
    campid= models.IntegerField(null=True)
    itemname=models.CharField(max_length=100,null=True)
    quantity=models.IntegerField(null=True)


class RescueTeam(models.Model):
    uid=models.IntegerField(null=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    date= models.DateField(null=True,blank=True)
    state = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
