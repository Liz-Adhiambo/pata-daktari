from multiprocessing import context
from django.shortcuts import render,redirect
from django.urls import reverse
from rest_framework import serializers, generics,viewsets
from rest_auth.registration.views import RegisterView
from core.forms import BookAppointmentForm, DoctorRegisterForm, LoginForm, PatientRegisterForm
from django.contrib.auth import login, logout, authenticate
from core.models import Doctor, Doctorblog, Patientappointment,User
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







#template views

def index(request):
    return render(request, 'home.html')


class doctorsRegistration(CreateView):
    model = User
    form_class = DoctorRegisterForm
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

    doctors=Doctor.objects.all()
    context={
        'doctors':doctors
    }

    return render(request,'patients/alldoctors.html',context)



def doctor_profile(request, username):  
    obj = User.objects.get(username=username)  
    appointments=Patientappointment.objects.filter(doctor=obj.doctor)
    context = {
        'username': obj, 
        'appointments': appointments
        
    }
   
    return render(request, 'doctors/doctorprofile.html',  context)

#patients profile
def patient_profile(request, username):  
    obj = User.objects.get(username=username)  
    appointments=Patientappointment.objects.filter(patient=obj.id)
    context = {
        'username': obj, 
        'appointments': appointments
        
    }
   
    return render(request, 'patients/patientprofile.html',  context)

def doctorblog_list(request):
    
        blogs = Doctorblog.objects.all()

        context={
            'blogs':blogs
        }
        return render(request, 'doctors/doctorblog.html', context)

        
        

class PostListView(ListView):
    model = Doctorblog
    template_name = 'doctors/doctorblog.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    


class PostDetailView(DetailView):
    model = Doctorblog
    template_name = 'doctors/doctorblog_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Doctorblog
    template_name = 'doctors/doctorblog_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.doctor = self.request.user 
        return super().form_valid(form)
    def get_success_url(self): # new
             return reverse('api:blog-home')

    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Doctorblog
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Doctorblog
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.doctor:
            return True
        return False
        

def logout(request):
    auth.logout(request)
    return redirect('core:indexy')

# appointemnt views
class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Patientappointment
    template_name = 'bookappointment.html'
    fields = ['doctor','date', 'time','reason_for_visit']

    def form_valid(self, form):
        form.instance.patient = self.request.user 
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
    template_name = 'profile.html'
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
    template_name = 'profile_list.html'

    def get(self, request):
        queryset = Doctor.objects.all()
        return Response({'profiles': queryset})