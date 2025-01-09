from django.db import models

# Create your models here.
class customer(models.Model):
    cid = models.AutoField(primary_key=True)
    username= models.CharField(max_length=50, unique=True)
    password= models.CharField(max_length=50,)
    full_name= models.CharField(max_length=150)
    email= models.EmailField(max_length=254,blank=True, unique=True)
    phone_number=models.BigIntegerField(blank=True, unique=True , null=True)
    profile_image= models.ImageField(blank=True,upload_to='profile')
    created_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default = False)
    class Meta:
        db_table = 'customer' 
        

class hostMaster(models.Model):
    hid = models.AutoField(primary_key=True)
    username= models.CharField(max_length=50, unique=True)
    password= models.CharField(max_length=50,)
    full_name= models.CharField(max_length=150)
    email= models.EmailField(max_length=254,blank=True, unique=True)
    phone_number=models.BigIntegerField(blank=True, unique=True , null=True)
    profile_image= models.ImageField(blank=True,upload_to='profile')
    created_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default = False)
    class Meta:
        db_table = 'hostMaster' 
    
class loanTypeMaster(models.Model):
    loantypeId = models.AutoField(primary_key=True)
    Lname = models.CharField(max_length=200)
    Intrest = models.CharField(max_length=100)
    

    

