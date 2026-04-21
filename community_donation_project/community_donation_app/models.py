from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)

class Donor(models.Model):
    donor_id=models.ForeignKey(Login,on_delete=models.CASCADE)
    username = models.CharField(max_length=20,null=True)
    name = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=30,null=True)
    address = models.TextField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    image = models.ImageField(upload_to='Image',null=True)

class Ngo(models.Model):
    ngo_id=models.ForeignKey(Login,on_delete=models.CASCADE)
    username = models.CharField(max_length=20,null=True)
    name = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=30,null=True)
    address = models.TextField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    image = models.ImageField(upload_to='Image',null=True)



class Donation(models.Model):
    ngo = models.ForeignKey('Ngo', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200,null=True)
    category = models.CharField(max_length=100,
        choices=[
            ('Food', 'Food'),
            ('Education', 'Education'),
            ('Medical', 'Medical Supplies'),
            ('Clothing', 'Clothing'),
            ('General', 'General'),
        ],
        default='General')
    
    target_amount = models.IntegerField(null=True,blank=True)
    current_amount = models.IntegerField(null=True,blank=True)
    donation_type = models.CharField(max_length=50, default="Monetary")
    image = models.ImageField(upload_to='donation_images/', null=True, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    location = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=50, default='Active',null=True)
    
class DonationTransaction(models.Model):
    donor = models.ForeignKey('Donor', on_delete=models.CASCADE)
    donation = models.ForeignKey('Donation', on_delete=models.CASCADE)
    donation_type = models.CharField(max_length=50,null=True)
    amount = models.IntegerField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=[
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
        ('card', 'Credit/Debit Card')
    ], null=True, blank=True)


class Chat(models.Model):
    donor_id = models.ForeignKey(Donor, on_delete=models.CASCADE)
    ngo_id = models.ForeignKey(Ngo, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    time = models.CharField(max_length=100)
    utype = models.CharField(max_length=100)
