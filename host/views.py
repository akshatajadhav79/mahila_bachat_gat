from django.shortcuts import render,redirect,HttpResponseRedirect
from host.models import hostMaster
from django.contrib import messages
import os
import datetime
from django.conf import settings
from django.http import JsonResponse
import face_recognition 

# Create your views here.

# for index page
def index(request):
    return render(request, "index.html", {'uid': "user"})

def host_home(request):
    return render(request, "host_home.html", {'uid': "user"})

def host_login(request):
    return render(request, "host_login.html", {'uid': "user"})

def host_reg(request):
    if request.method == "POST":
        fname = request.POST.get('username')
        contact = request.POST.get('contact')
        email1 = request.POST.get('email')
        password1 = request.POST.get('password')
        username1 = request.POST.get('username')
        cpassword1 = request.POST.get('password1')
        profile_img = request.FILES.get('profile_image')
        
        # Check if username or email already exists in the database
        if hostMaster.objects.filter(email=email1).exists():
            messages.error(request, 'Email is already taken')
            return redirect(request.path_info)
        elif hostMaster.objects.filter(username=username1).exists():
            messages.error(request, 'Username is already taken')
            return redirect(request.path_info)

        # Check if the passwords match
        elif password1 != cpassword1:
            messages.error(request, "Confirm password does not match")
            return redirect(request.path_info)

        else:
            try:
                # Hash the password before saving
                # hashed_password = make_password(password1)

                # Create the hostMaster instance and save to the database
                cust = hostMaster.objects.create(
                    username=username1,
                    password=cpassword1,
                    full_name=fname,
                    email=email1,
                    phone_number=contact,
                    profile_image=profile_img,
                    is_active=True
                )
                cust.save()
                messages.success(request, "Your account has been created successfully!")
                return redirect("/hostMaster/cust_login")

            except Exception as e:
                # Capture detailed error
                error_message = str(e)  # Get the exception message
                print(f"Error occurred: {error_message}")
                messages.error(request, f"An error occurred while saving your data: {error_message}")
                return redirect(request.path_info)
              
    return render(request,"cust_register.html")


