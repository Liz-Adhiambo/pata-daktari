from . import views
from django.urls import path
from . import views
from django.conf import settings


from django.urls import path
from core.views import AppointmentCreateView, DoctorRegistrationView, PatientRegistrationView, PostCreateView, PostDeleteView, PostDetailView, PostListView, PostUpdateView,ProfileAPI, doctorsRegistration, patientsRegistration
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



app_name = 'core'

urlpatterns = [
    path('', views.index,name='indexy'),
    path('registering/', doctorsRegistration.as_view(), name='doctors'),
    path('registering-patients/', patientsRegistration.as_view(), name='patients'),
    path('login-doctor/', views.login_view, name='logindoctor'),
    path('doctor/<str:username>/', views.doctor_profile, name='doctorprofile'),
    path('patient/<str:username>/', views.patient_profile, name='patientprofile'),
    path('patientprofile/', AppointmentCreateView.as_view(), name='bookappointment'),
    path('blogs',views.doctorblog_list, name='blogs'),
    path('doctor/posts', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('logout/', views.logout, name='logout'),
    path('finddoctors/', views.all_doctors, name='alldoctors'),
    



    #Registration Urls
    path('registration/doctor/', DoctorRegistrationView.as_view(), name='register-doctor'),
    path('registration/patient/', PatientRegistrationView.as_view(), name='register-patient'),
    # path('profile/',ProfileView.as_view()),
    path('users/<user_id>/profile/', ProfileAPI.as_view()),
    path('blogs', views.blog_list),
    path('blogs/<pk>', views.blog_detail),
    path('blogs/published', views.blog_list_published),
    path('profiles',views.ProfileList.as_view(), name='doctors profiles'),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()