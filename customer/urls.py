from django.urls import path,include
from customer.views import *

urlpatterns = [
    path('cust_login/',cust_login,name='cust_login'),
    path('cust_register/',cust_register,name ='cust_register'),
    path('custadmin/',custadmin,name='custadmin'),
    
    path('f_login/',f_login,name="f_login"),
    path('face_login/<str:username>/', face_login, name='face_login'),
    path('cust_logout/', cust_logout,name='cust_logout'),
    path('cust_forgetPass/', cust_forgetPass,name='cust_forgetPass'),
    
] 