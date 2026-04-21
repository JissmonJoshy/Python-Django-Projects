from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)

class Police_department(models.Model):
    user=models.ForeignKey(Login, on_delete=models.CASCADE)
    username = models.CharField(max_length=30,null=True)
    name=models.CharField(max_length=50,null=True)
    address = models.TextField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    image = models.ImageField(upload_to='Police',null=True)

class User(models.Model):
    user=models.ForeignKey(Login, on_delete=models.CASCADE)
    username = models.CharField(max_length=30,null=True)
    name=models.CharField(max_length=50,null=True)
    address = models.TextField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    image = models.ImageField(upload_to='User',null=True)


class Law(models.Model):
    police = models.ForeignKey(Police_department, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Police_department, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='Complaints/', null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending')  # Pending, In Progress, Resolved
    date_submitted = models.DateTimeField(auto_now_add=True)


class MissingPerson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Police_department, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=100)
    age = models.IntegerField()
    last_seen_location = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='MissingPersons/', null=True, blank=True)
    status = models.CharField(max_length=50, default='Unresolved')
    date_reported = models.DateTimeField(auto_now_add=True)
    address = models.TextField(null=True)
    pincode = models.CharField(max_length=10, null=True)


class CrimeReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Police_department, on_delete=models.CASCADE)
    crime_type = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField()
    evidence = models.FileField(upload_to='CrimeReports/', null=True, blank=True)
    status = models.CharField(max_length=50, default='Under Investigation')
    date_reported = models.DateTimeField(auto_now_add=True)


class CaseReport(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, null=True, blank=True)
    missing_person = models.ForeignKey(MissingPerson, on_delete=models.CASCADE, null=True, blank=True)
    crime_report = models.ForeignKey(CrimeReport, on_delete=models.CASCADE, null=True, blank=True)

    police = models.ForeignKey(Police_department, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to='Reports/', null=True)
    case_evidence = models.TextField()
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)