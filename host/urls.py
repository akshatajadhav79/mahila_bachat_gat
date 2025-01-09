from django.urls import path,include
from host.views import *

urlpatterns = [
    
    path('',index,name="index"),
    path('hosthome/',host_home,name="hosthome"),
    path('host_login/',host_login,name="host_login"),
    path('host_reg/',host_reg,name="host_reg"),
] 