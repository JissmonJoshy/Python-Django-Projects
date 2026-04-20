from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)

class Teacher(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField(unique=True)
    batch = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='teacher_profiles/', null=True, blank=True)


class Student(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    batch = models.CharField(max_length=50, blank=True)
    year = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='student_profiles/', null=True, blank=True)
    assigned_teacher = models.ForeignKey(
        'Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='students'
    )

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('Absent', 'Absent')],
        default='Absent'
    )
    time_slot = models.CharField(
        max_length=20,
        choices=[('10-11', '10-11 AM'), ('11-12', '11-12 AM'), ('2-3', '2-3 PM')],  # extend as needed
        default='10-11'
    )

    class Meta:
        unique_together = ('student', 'date', 'time_slot')  # Prevent duplicate attendance for same date and time slot