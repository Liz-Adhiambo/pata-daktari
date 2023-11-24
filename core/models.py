from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField

class User(AbstractUser):
  #Boolean fields to select the type of account.
  is_doctor = models.BooleanField(default=False)
  is_patient = models.BooleanField(default=False)

class Doctor(models.Model):
    doctor = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    hospital = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    description = models.TextField()
    profile_pic = CloudinaryField('image',blank=True)
    address = models.CharField(max_length=100,null=True)
    years_of_experience = models.CharField(max_length=100,null=True)
    speciality = models.CharField(max_length=100,blank=True)
    


    

    def __str__(self):
        return self.doctor.username

    


class Patient(models.Model):
    patient = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    profile_pic = CloudinaryField('image', blank=True)
    address = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.patient.username

class Doctorblog(models.Model):
    doctor= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=70, blank=False, default='')
    # content = models.TextField(blank=False, default='')
    content = RichTextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    blog_pic = CloudinaryField('image', blank=True)


    #appointment models

TIMESLOT_LIST = (
        ( '1','09:00 - 10:00'),
        ( '2','10:00 - 11:00'),
        ('3', '11:00 - 12:00'),
        ('4', '2:00 - 3:00'),
        ('5', '3:00 - 4:00'),
    )
class Patientappointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, related_name='doctor_appointments')
    date = models.DateTimeField()
    time = models.CharField(max_length=50, choices=TIMESLOT_LIST, null=True)
    reason_for_visit = models.CharField(max_length=255, null=True)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='patient_appointments')
    phone_number = models.CharField(max_length=50, null=True)
    email=models.EmailField(null=True, blank=True, max_length=100)
    


    
TYPE_TEST= (
        ('Comprehensive', 'Comprehensive Test'),
        ('Basic Test','Basic test'),
)
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female')
    ]
class LabTest(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    test = models.CharField(max_length=50, choices=TYPE_TEST, null=True)
    gender = models.CharField(max_length=50,choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=100)
    date_of_birth = models.DateTimeField()
    email=models.EmailField(null=True, blank=True, max_length=100)
      
    