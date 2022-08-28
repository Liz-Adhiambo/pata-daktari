from dj_rest_auth.registration.views import RegisterView
from django.shortcuts import render,redirect
from django.urls import reverse
from dj_rest_auth import serializers
from core.forms import BookAppointmentForm, DoctorProfileUpdateForm, DoctorRegisterForm, LabTestForm, LoginForm, PatientRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth import login, logout, authenticate
from core.models import Doctor, Doctorblog, LabTest, Patient, Patientappointment,User
from rest_framework.renderers import TemplateHTMLRenderer
from core.serializers import (
    DoctorCustomRegistrationSerializer, PatientCustomRegistrationSerializer,ProfileSerializer,DoctorblogSerializer
    )
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import ContactForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


#sendgrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


#sendgrid view





#contact view

   


#template views

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            html = render_to_string('contact/emails/contactform.html', {
                'name': name,
                'email': email,
                'subject': subject,
                'content': content
            })
            send_mail('The contact form subject', 'This is the message', 'noreply@codewithstein.com', [email], html_message=html)
            messages.success(request, 'Your message was sent successfully!')  
            return redirect('api:indexy')
        else:
            messages.warning(request, 'Please correct the error below.') 
            
    else:
        form = ContactForm()
    return render(request, 'home.html', {
        'form': form
    })




    


class doctorsRegistration(SuccessMessageMixin,CreateView):
    model = User
    form_class = DoctorRegisterForm
    success_url = reverse_lazy('core:logindoctor')
    success_message = " Your Account has been created successfully"
    template_name ='doctors/register.html'
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        
        return redirect('core:logindoctor')

class patientsRegistration(CreateView):
    model = User
    form_class = PatientRegisterForm
    template_name ='patients/registers.html'
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('core:logindoctor')


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None and user.is_doctor:
                login(request, user)
                return redirect('core:doctorprofile',username)
            elif user is not None and user.is_patient:
                login(request, user)
                return redirect('core:alldoctors')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

def all_doctors(request):

    doctors_list=Doctor.objects.all()
    

    page = request.GET.get('page', 1)
    paginator = Paginator(doctors_list, 3)

    try:
        doctors = paginator.page(page)
    except PageNotAnInteger:
        doctors = paginator.page(1)
    except EmptyPage:
        doctors = paginator.page(paginator.num_pages)



    context={
        'doctors':doctors,
        
    }

    return render(request,'patients/alldoctors.html',context)



# doctor login

@login_required(login_url='core:logindoctor')
def doctor_profile(request, username):  
    obj = User.objects.get(username=username)  
    appointments=Patientappointment.objects.filter(doctor__exact=request.user)
    context = {
        'username': obj, 
        'appointments': appointments
        
    }
   
    return render(request, 'doctors/doctorprofile.html',  context)

#patients profile
@login_required(login_url='core:logindoctor')
def patient_profile(request, username):  
    obj = User.objects.get(username=username)  
    appointments=Patientappointment.objects.filter(patient=obj.id)
    labtests=LabTest.objects.filter(patient=obj.id)
    context = {
        'username': obj, 
        'appointments': appointments,
        'labtests':labtests
        
    }
   
    return render(request, 'patients/patientprofile.html',  context)

def doctorblog_list(request):
    
        blog_list = Doctorblog.objects.all()

        page = request.GET.get('page', 1)
        paginator = Paginator(blog_list, 4)

        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        context={
            'blogs':blogs
        }
        return render(request, 'doctors/doctorblog.html', context)

        
        

class PostListView(ListView):
    model = Doctorblog
    template_name = 'doctors/doctorblog.html'  
    context_object_name = 'posts'
    paginate_by = 10
    queryset = Doctorblog.objects.all()


class PostDetailView(DetailView):
    model = Doctorblog
    template_name = 'doctors/doctorblog_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Doctorblog
    template_name = 'doctors/doctorblog_form.html'
    fields = ['title', 'content','blog_pic']

    def form_valid(self, form):
        form.instance.doctor = self.request.user 
        return super().form_valid(form)
    def get_success_url(self): # new
             return reverse('api:blogs')

    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Doctorblog
    template_name = 'doctors/doctorblog_form.html'
    fields = ['title', 'content','blog_pic']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.doctor:
            return True
        return False
    
    def get_success_url(self): # new
             return reverse('api:blogs')


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Doctorblog
    template_name = 'doctors/doctordelete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.doctor:
            return True
        return False
        
@login_required(login_url='core:logindoctor')
def logout(request):
    auth.logout(request)
    return redirect('core:indexy')

@login_required(login_url='core:logindoctor')
def update_profile(request):
    Patient.objects.get_or_create(patient=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.patient)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.instance.user=request.user
            p_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('core:indexy')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm()

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'patients/update_profile.html', context) 
    
@login_required(login_url='logindoctor')
def doctorupdate_profile(request):
    Doctor.objects.get_or_create(doctor=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        pr_form = DoctorProfileUpdateForm(request.POST, request.FILES, instance=request.user.doctor)
        if u_form.is_valid() and pr_form.is_valid():
            u_form.save()
            pr_form.instance.user=request.user
            pr_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('core:indexy')

    else:
        u_form = UserUpdateForm(instance=request.user)
        pr_form = DoctorProfileUpdateForm()

    context = {
        'u_form': u_form,
        'pr_form': pr_form
    }

    return render(request, 'doctors/update_profile.html', context)   


#labtest views
def labtests(request):

    return render(request,'labtest.html')

class LabtestCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login-doctor/'
    model = LabTest
    template_name = 'labtestform.html'
    fields = ['test','gender', 'phone_number','date_of_birth','email']

    def form_valid(self, form):
        form.instance.patient = self.request.user 
        email=form.cleaned_data['email']
        name=self.request.user 
        message = Mail(
            from_email='gladys.wangi@student.moringaschool.com',
            to_emails=[email],
            subject='You have successfully booked an appointment.',
            html_content='you have booked an appointment with patadaktari')
        
        message.template_id='d-513767008d3e4adb865afe88112aabd3'
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

        
        return super().form_valid(form)
    def get_success_url(self): # new
        
             return reverse('api:indexy')
    
    

# appointemnt views

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login-doctor/'
    model = Patientappointment
    template_name = 'bookappointment.html'
    fields = ['doctor','date', 'time','reason_for_visit','email']

    def form_valid(self, form):
        form.instance.patient = self.request.user 
        email=form.cleaned_data['email']
        name=self.request.user 
        message = Mail(
            from_email='gladys.wangi@student.moringaschool.com',
            to_emails=[email],
            subject='You have successfully booked an appointment.',
            html_content='you have booked an appointment with patadaktari')
        
        message.template_id='d-0e8a0b14bbd042278a3ff89c3a99a1e9'
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

                    
        return super().form_valid(form)
    def get_success_url(self): # new
        
             return reverse('api:indexy')






#api views
class DoctorRegistrationView(RegisterView):
    
    serializer_class = DoctorCustomRegistrationSerializer


class PatientRegistrationView(RegisterView):
    serializer_class = PatientCustomRegistrationSerializer

# class ProfileView(generics.RetrieveAPIView):
#     serializer_class = ProfileSerializer

#     def get_object(self):
#         return self

class ProfileAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        profile_serializer = ProfileSerializer(user.doctor)
        return Response(profile_serializer.data)

@api_view(['GET', 'POST', 'DELETE'])
def blog_list(request):
    if request.method == 'GET':
        blogs = Doctorblog.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            blogs = blogs.filter(title__icontains=title)
        
        blogs_serializer = DoctorblogSerializer(blogs, many=True)
        return JsonResponse(blogs_serializer.data, safe=False)
        # 'safe=False' for objects serialization

 
    elif request.method == 'POST':
        blog_data = JSONParser().parse(request)
        
        blog_serializer = DoctorblogSerializer(data=blog_data,context={'request': request})
        
        
        if blog_serializer.is_valid():

            blog_serializer.save()
            return JsonResponse(blog_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(blog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Doctorblog.objects.all().delete()
        return JsonResponse({'message': '{} blogss were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'PUT', 'DELETE'])
def blog_detail(request, pk):
    # find tutorial by pk (id)
    try: 
        blog = Doctorblog.objects.get(pk=pk) 
        
    except Doctorblog.DoesNotExist: 
        return JsonResponse({'message': 'The blog does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
       blog_serializer = DoctorblogSerializer(blog) 

       return JsonResponse(blog_serializer.data) 
    elif request.method == 'PUT': 
        blog_data = JSONParser().parse(request) 
        blog_serializer = DoctorblogSerializer(blog, data=blog_data) 
        if blog_serializer.is_valid(): 
            blog_serializer.save() 
            return JsonResponse(blog_serializer.data) 
        return JsonResponse(blog_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'DELETE': 
        blog.delete() 
        return JsonResponse({'message': 'Blog was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
 
    # GET / PUT / DELETE tutorial
    
@api_view(['GET'])
def blog_list_published(request):
    blogs = Doctorblog.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = DoctorblogSerializer(blogs, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)

class ProfileList(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        queryset = Doctor.objects.all()
        return Response({'profiles': queryset})