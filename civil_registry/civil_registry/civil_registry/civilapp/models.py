from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore


# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=20)
    viewpassword=models.CharField(max_length=20)
class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    district = models.CharField(max_length=100,null=True)
    aadhar = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=6,null=True)
    user=models.ForeignKey(Login,on_delete=models.CASCADE,null=True)


class Addauthority(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    district = models.CharField(max_length=100,null=True)
    taluk = models.CharField(max_length=100,null=True)
    authority = models.CharField(max_length=100,null=True)
    user=models.ForeignKey(Login,on_delete=models.CASCADE,null=True)

class Birth(models.Model):
    name = models.CharField(max_length=255)
    father = models.CharField(max_length=255)
    mother = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    birthplace = models.CharField(max_length=255)
    birth = models.CharField(max_length=10)
    relation = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True,null=True)
    district = models.CharField(max_length=255)
    taluk = models.CharField(max_length=255,null=True)
    address = models.CharField(max_length=300)
    identification = models.CharField(max_length=20)
    idproof = models.FileField(upload_to="uploadfiles",max_length=None,null=True)
    user=models.ForeignKey(Registration,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,default='pending')
    payment_status=models.CharField(max_length=100,default='pending')
    certificate = models.FileField(upload_to="uploadfiles",max_length=None,null=True)
    father_address = models.TextField(null=True)
    mother_address = models.TextField(null=True)

    father_phone = models.CharField(max_length=15, null=True)
    mother_phone = models.CharField(max_length=15, null=True)

    father_email = models.EmailField(null=True)
    mother_email = models.EmailField(null=True)

    father_blood = models.CharField(max_length=5, null=True)
    mother_blood = models.CharField(max_length=5, null=True)
    child_blood = models.CharField(max_length=5, null=True)

    father_idproof = models.FileField(upload_to="uploadfiles", null=True)
    mother_idproof = models.FileField(upload_to="uploadfiles", null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)



class Death(models.Model):
    name = models.CharField(max_length=255)
    father = models.CharField(max_length=255)
    mother = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    relation = models.CharField(max_length=10)
    dob = models.DateField()
    dod = models.DateField()
    deathplace = models.CharField(max_length=255)
    taluk = models.CharField(max_length=255,null=True)
    death = models.CharField(max_length=10)
    district = models.CharField(max_length=255)
    address = models.CharField(max_length=300)
    identification = models.CharField(max_length=255)
    idproof = models.FileField(upload_to="uploadfiles",max_length=None,null=True)
    type = models.CharField(max_length=255)
    status=models.CharField(max_length=100,default='pending')
    user=models.ForeignKey(Registration,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    payment_status=models.CharField(max_length=100,default='pending')
    certificate = models.FileField(upload_to="uploadfiles",max_length=None,null=True)



    father_address = models.TextField(null=True)
    mother_address = models.TextField(null=True)

    father_phone = models.CharField(max_length=15, null=True)
    mother_phone = models.CharField(max_length=15, null=True)

    father_email = models.EmailField(null=True)
    mother_email = models.EmailField(null=True)

    father_blood = models.CharField(max_length=5, null=True)
    mother_blood = models.CharField(max_length=5, null=True)

    father_idproof = models.FileField(upload_to="uploadfiles", null=True)
    mother_idproof = models.FileField(upload_to="uploadfiles", null=True)

    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)


class Marriage(models.Model):
    bridename = models.CharField(max_length=255)
    bridefather =models.CharField(max_length=255)
    bridemother = models.CharField(max_length=255)
    bridedob= models.DateField()
    taluk = models.CharField(max_length=255,null=True)
    brideaddress=models.CharField(max_length=300)
    groomname =models.CharField(max_length=255) 
    groomfather = models.CharField(max_length=255)
    groommother = models.CharField(max_length=255)
    groomdob= models.DateField()
    groomaddress=models.CharField(max_length=300)
    marriagedate = models.DateField()
    marriageplace = models.CharField(max_length=255)
    marriagetype =models.CharField(max_length=255)
    relation= models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True,null=True)
    district = models.CharField(max_length=255)
    address =models.CharField(max_length=300)
    idproofbride =models.FileField(upload_to="uploadfiles",max_length=None,null=True)
    idproofgroom =models.FileField(upload_to="uploadfiles",max_length=None,null=True)
    status=models.CharField(max_length=100,default='pending')
    user=models.ForeignKey(Registration,on_delete=models.CASCADE,null=True)
    payment_status=models.CharField(max_length=100,default='pending')
    certificate = models.FileField(upload_to="uploadfiles",max_length=None,null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

class License(models.Model):
    name = models.CharField(max_length=255)
    father = models.CharField(max_length=255)
    mother = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    place = models.CharField(max_length=255)
    blood = models.CharField(max_length=10)
    klno = models.CharField(max_length=10)
    district = models.CharField(max_length=255)
    address = models.CharField(max_length=300)
    identification = models.CharField(max_length=20)
    idproof = models.FileField(upload_to="uploadfiles",max_length=None,null=True)
    user=models.ForeignKey(Registration,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,default='pending')
    date = models.DateTimeField(auto_now_add=True,null=True)
    photo = models.FileField(upload_to="uploadimages",max_length=None,null=True)
    payment_status=models.CharField(max_length=100,default='pending')

    father_email = models.EmailField(null=True)
    father_phone = models.CharField(max_length=15, null=True)
    father_address = models.TextField(null=True)
    father_proof = models.FileField(upload_to="uploadfiles", null=True)

    mother_email = models.EmailField(null=True)
    mother_phone = models.CharField(max_length=15, null=True)
    mother_address = models.TextField(null=True)
    mother_proof = models.FileField(upload_to="uploadfiles", null=True)

    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    certificate = models.FileField(upload_to="uploadfiles", null=True)

class Passport(models.Model):
    name = models.CharField(max_length=100)
    father = models.CharField(max_length=100)
    mother = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    place = models.CharField(max_length=100)
    blood = models.CharField(max_length=5)
    district = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    identification = models.CharField(max_length=100)
    idproof = models.FileField(upload_to="uploadfiles",max_length=None,null=True)
    photo = models.FileField(upload_to="uploadimages",max_length=None,null=True)
    addressproof = models.FileField(upload_to="uploadfiles",max_length=None,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    user=models.ForeignKey(Registration,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,default='pending')
    payment_status=models.CharField(max_length=100,default='pending')
    martial= models.CharField(max_length=100)

    father_email = models.EmailField(null=True)
    father_phone = models.CharField(max_length=15, null=True)
    father_address = models.TextField(null=True)
    father_proof = models.FileField(upload_to="uploadfiles", null=True)

    mother_email = models.EmailField(null=True)
    mother_phone = models.CharField(max_length=15, null=True)
    mother_address = models.TextField(null=True)
    mother_proof = models.FileField(upload_to="uploadfiles", null=True)

    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    certificate = models.FileField(upload_to="uploadfiles", null=True, blank=True)

class Voters(models.Model):
    name = models.CharField(max_length=100)
    father = models.CharField(max_length=100)
    mother = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    place = models.CharField(max_length=100)
    blood = models.CharField(max_length=5)
    district = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    identification = models.CharField(max_length=100)
    idproof = models.FileField(upload_to="uploadfiles",max_length=None,null=True)
    photo = models.FileField(upload_to="uploadimages",max_length=None,null=True)
    addressproof = models.FileField(upload_to="uploadfiles",max_length=None,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    user=models.ForeignKey(Registration,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,default='pending')
    payment_status=models.CharField(max_length=100,default='pending')
    martial= models.CharField(max_length=100)

    father_email = models.EmailField(null=True)
    father_phone = models.CharField(max_length=15, null=True)
    father_address = models.TextField(null=True)
    father_proof = models.FileField(upload_to="uploadfiles", null=True)

    mother_email = models.EmailField(null=True)
    mother_phone = models.CharField(max_length=15, null=True)
    mother_address = models.TextField(null=True)
    mother_proof = models.FileField(upload_to="uploadfiles", null=True)

    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    certificate = models.FileField(upload_to="uploadfiles", null=True, blank=True)

class Feedback(models.Model):
    feedback = models.CharField(max_length=300)
    user=models.ForeignKey(Registration,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    
class Assign(models.Model):
    birth=models.ForeignKey(Birth,on_delete=models.CASCADE,null=True)
    death=models.ForeignKey(Death,on_delete=models.CASCADE,null=True)
    marriage=models.ForeignKey(Marriage,on_delete=models.CASCADE,null=True)
    registrar=models.ForeignKey(Addauthority,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,default='pending')
 
