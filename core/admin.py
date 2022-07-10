from django.contrib import admin
from core.models import  Doctor, LabTest, Patient, Patientappointment, User,Doctorblog
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Doctorblog)
admin.site.register(Patientappointment)
admin.site.register(LabTest)