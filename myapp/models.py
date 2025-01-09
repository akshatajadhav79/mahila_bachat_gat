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