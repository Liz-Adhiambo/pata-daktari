import datetime
from django import forms
from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from crispy_forms.layout import Layout, Div
from .models import  LabTest, Patient, Patientappointment, User, Doctor
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput

class DoctorRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username= forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.is_doctor = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username=self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.save() 
        doctor = Doctor.objects.create(doctor=user)
        doctor.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

class PatientRegisterForm(UserCreationForm):
    
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username= forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.is_patient = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username=self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.save() 
        patient = Patient.objects.create(patient=user)
        patient.save()
        return user



class BookAppointmentForm(forms.ModelForm):
    date=forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Patientappointment
        fields = ['doctor', 'date', 'time', 'reason_for_visit']
        labels = {
            'doctor':'please select your doctor',
            'date': 'date(YYYY/MM/DD)',
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.label_class = 'sr-only'
    #     self.helper.form_tag = False
    #     self.helper.layout = Layout(
    #     PrependedText('doctor', '<i class="fa fa-home"></i>', placeholder="Building Number or Name",
    #                   ),
    #     PrependedText('date', '<i class="fa fa-home"></i>', placeholder="Street Name",
    #                   ),
    #     PrependedText('time', '<i class="fa fa-home"></i>', placeholder="Town or City",
    #                   label="test"),
    #     PrependedText('reason_for_visit', '<i class="fa fa-home"></i>', placeholder="County"),
    # )

    # class Meta:
    #     model = Patientappointment
    #     fields = ['doctor', 'date', 'time', 'reason_for_visit',
                
    #             ]
    #     labels = {
    #         'date': 'Have you lived at the property for 3 years?',
    #     } 

class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ('__all__')



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['phone', 'profile_pic', 'address']

class DoctorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        
        fields = ['hospital','phone', 'description','profile_pic','address','years_of_experience','speciality']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    subject = forms.CharField(max_length=80)
    content = forms.CharField(widget=forms.Textarea)