from django import forms
from crispy_forms.helper import FormHelper
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
    class Meta:
        model = Patientappointment
        fields = ['doctor', 'date', 'time', 'reason_for_visit']
    #     date = forms.DateField(
    #     widget=DatePickerInput(format='%m/%d/%Y')
    # )
class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ('__all__')