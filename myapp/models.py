from django.db import models
from django.conf import settings

# Create your models here.

class User_master(models.Model):
    viewer_id = models.BigAutoField(primary_key=True)
    username= models.CharField(max_length=50, unique=True)
    password= models.CharField(max_length=50,)
    full_name= models.CharField(max_length=150)
    email= models.EmailField(max_length=254,blank=True, unique=True)
    phone_number=models.BigIntegerField(blank=True, unique=True , null=True)
    user_profile_image= models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default = False)
    address = models.TextField(blank=True, null=True)
    
class ViewerSession(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.CharField(max_length=255)  # unique session ID
    viewer = models.ForeignKey(User_master, on_delete=models.CASCADE, related_name='viewer_sessions')
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

class host_master(models.Model):
    username= models.CharField(max_length=50, unique=True)
    password= models.CharField(max_length=50,)
    full_name= models.CharField(max_length=150)
    email= models.EmailField(max_length=254,blank=True, unique=True)
    phone_number=models.BigIntegerField(blank=True, unique=True , null=True)
    created_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default = False)
    address = models.TextField(blank=True, null=True)
    h_img = models.ImageField(blank=True,upload_to="hostpic")
    
class cust_master(models.Model):
    username= models.CharField(max_length=50, unique=True)
    password= models.CharField(max_length=50,)
    full_name= models.CharField(max_length=150)
    email= models.EmailField(max_length=254,blank=True, unique=True)
    phone_number=models.BigIntegerField(blank=True, unique=True , null=True)
    created_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default = False)
    address = models.TextField(blank=True, null=True)
    c_img = models.ImageField(blank=True,upload_to="custpic")
    
class service_master(models.Model):
    sname= models.CharField(max_length=50, unique=True)
    s_image= models.ImageField(blank=True,upload_to='service_img')
    created_date = models.DateField(auto_now_add=True)
    info = models.TextField(blank=True, null=True)
    
class contact_master(models.Model):
    name= models.CharField(max_length=50, unique=True)
    email= models.EmailField(max_length=254,blank=True, unique=True)
    phone_number=models.BigIntegerField(blank=True, unique=True , null=True)
    msg = models.TextField(blank=True, null=True)
    
    
    