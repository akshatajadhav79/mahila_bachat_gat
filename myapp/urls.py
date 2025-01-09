from django.urls import path,include
from myapp.views import *

urlpatterns = [
    path('userLogin',user_login,name=''),
    path('',home,name='home'),
    path('video/',video,name='video'),
    path('opencJS/',opencJS,name='opencJS'),
    path('process_image/', process_image, name='process_image'),
    path('10min/', min10, name='10min'),
    path('face_login/<str:username>/', face_login, name='face_login'),
    path('logout/', logout, name='logout'),
   
    path('contact/',contact,name='contact'),
    path('Deposit/<str:service>',Deposit,name='Deposit'),
    path('Loan/<str:loan>',Loan,name='Loan'),
    path('careers/',careers,name='careers'),
    path('otherser/',otherser,name='otherser'),

  
] 