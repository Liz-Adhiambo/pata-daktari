
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token

from core.models import Doctor, Patient,Doctorblog

class DoctorCustomRegistrationSerializer(RegisterSerializer):
    doctor = serializers.PrimaryKeyRelatedField(read_only=True,) #by default allow_null = False
    hospital = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    
    def get_cleaned_data(self):
            data = super(DoctorCustomRegistrationSerializer, self).get_cleaned_data()
            extra_data = {
                'hospital' : self.validated_data.get('hospital', ''),
                'phone' : self.validated_data.get('phone', ''),
                'description': self.validated_data.get('description', ''),
            }
            data.update(extra_data)
            return data

    def save(self, request):
        user = super(DoctorCustomRegistrationSerializer, self).save(request)
        user.is_doctor = True
        user.save()
        doctor =Doctor(doctor=user, hospital=self.cleaned_data.get('hospital'), 
                phone=self.cleaned_data.get('phone'),
                description=self.cleaned_data.get('description'))
        doctor.save()
        return user


class PatientCustomRegistrationSerializer(RegisterSerializer):
    patient = serializers.PrimaryKeyRelatedField(read_only=True,) #by default allow_null = False
    phone = serializers.CharField(required=True)
    
    def get_cleaned_data(self):
            data = super(PatientCustomRegistrationSerializer, self).get_cleaned_data()
            extra_data = {
                'phone' : self.validated_data.get('phone', ''),
            }
            data.update(extra_data)
            return data

    def save(self, request):
        user = super(PatientCustomRegistrationSerializer, self).save(request)
        user.is_patient = True
        user.save()
        patient = Patient(patient=user,phone=self.cleaned_data.get('phone'))
        patient.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = (
            'doctor',
            'hospital',
            'phone',
            'description',
        )


class DoctorblogSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Doctorblog
        fields = ('id',
                  'doctor',
                  'title',
                  'content',
                  'published',
                  'created_at',)

        def create(self, **kwargs):
            """Include default for read_only `user` field"""
            kwargs["doctor"] = self.fields["doctor"].get_default()
            return super().create(**kwargs)