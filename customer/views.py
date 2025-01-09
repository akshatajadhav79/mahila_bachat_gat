import traceback
from django.shortcuts import render,redirect,HttpResponseRedirect
from host.models import customer
from django.contrib import messages
import os
import datetime
from django.conf import settings
from django.http import JsonResponse
import face_recognition 
import logging
from pathlib import Path
from django.core.mail import EmailMessage,send_mail

# Set up logger
logger = logging.getLogger(__name__)

# Create your views here.
def custadmin(request):
    user_id = request.session.get('user_id')
    print(request.session.get('user_id'))
    context = {}  # Initialize context dictionary
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/customer/cust_login')

    # Retrieve the user object based on the user_id stored in the session
    user = customer.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        # Handle the form submission if any
        if 'submit' in request.POST and request.POST['submit'] == 'Search':
            print("search")
            # Add logic for searching or any other actions

            # Update context with relevant data
            context = {"service": "service", "uid": user}  # Include user data in context
    else:
        # User not found, redirect to login page
        messages.error(request, "User not found.")
        return redirect('/customer/cust_login')
    return render(request,"cust_home.html",context)

def cust_login(request):
    if request.method == "POST":
        username1=request.POST.get('username')
        password1= request.POST.get('password')
        
        if 'submit' in request.POST and request.POST['submit'] == "Sign_in":
            if not customer.objects.filter(username=username1).exists():
                messages.error(request,"Invalid Username ")
                return redirect('/customer/cust_login') 
            else:
                usern = customer.objects.filter(username=username1).exists()
                if usern == True:
                    user=customer.objects.get(username=username1)
                    if user.password == password1:
                        request.session['user_id'] = user.pk
                        request.session['user_email'] = user.email
                        return redirect(f"/customer/custadmin")
                    else:
                        messages.error(request,"Wronge Password.")
                
        # Attempt to find the user by username   #################### this is by pymongo use in functions
        # user = con.find_one({"username": username1})
        # print(user)
        
        # if user:
        #     # Check if the password matches using Django's password checking system
        #     if password1 == user['password'] :
        #         # Store user details in the session
        #         request.session['user_id'] = str(user['_id'])  # Assuming _id is ObjectId
        #         request.session['user_email'] = user['emailID']
        #         request.session['user_role'] = "customer"  # Fixed typo: "custmer" -> "customer"
                
        #         # Redirect to customer admin page
        #         return redirect("/customer/custadmin")
        #     else:
        #         messages.error(request, "Wrong password.")
        #         return HttpResponseRedirect(request.path_info)
        # else:
        #     messages.error(request, "Invalid username.")
        #     return HttpResponseRedirect(request.path_info) 
    return render(request,"cust_login.html")

# TO registration
# to add validation in html and alert box updation
def cust_register(request):
    if request.method == "POST":
        fname = request.POST.get('username')
        contact = request.POST.get('contact')
        email1 = request.POST.get('email')
        password1 = request.POST.get('password')
        username1 = request.POST.get('username')
        cpassword1 = request.POST.get('password1')
        profile_img = request.FILES.get('profile_image')
        
        # Check if username or email already exists in the database
        if customer.objects.filter(email=email1).exists():
            messages.error(request, 'Email is already taken')
            return redirect(request.path_info)
        elif customer.objects.filter(username=username1).exists():
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

                # Create the customer instance and save to the database
                cust = customer.objects.create(
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
                return redirect("/customer/cust_login")

            except IntegrityError as e:
                messages.error(request, "This email or username is already taken.")
                print(f"IntegrityError: {str(e)}")
                return redirect(request.path_info)
            except Exception as e:
                # Capture detailed error
                error_message = str(e)  # Get the exception message
                tb = traceback.format_exc()  # Capture the full traceback
                print(f"Error occurred: {error_message}")
                print(f"Traceback: {tb}")
                messages.error(request, f"An error occurred while saving your data: {error_message}")
                return redirect(request.path_info)
              
         
        # if con.find({"emailID":email1,"username":username1}):
        #     messages.error(request,'Username is Already taken')
        #     return HttpResponseRedirect(request.path_info)
        # elif password1 != cpassword1:
        #     messages.error(request,"Confirm password does not match")
        #     return HttpResponseRedirect(request.path_info)
        # else:
        #     con.insert_one({"full_name":fname , "contact":contact ,"emailID":email1,"username":username1,"password":password1})
        #     messages.success(request,"Your account is created Successfully.Thank you for visit..!")
        #     return redirect("/customer/cust_login")
    return render(request,"cust_register.html")

def f_login(request):
    return render(request,"cust_login.html",{"fc":"fcLogin"})

# TO face check code
def face_login(request, username):
    
    print("faceLogin::::", username)
        
    # Check if image is uploaded
    if not request.FILES.get('image'):
        print("not image")
        return JsonResponse({'status': 'failure', 'message': 'Image is required'}, status=400)
    
    # username
    if not username and not customer.objects.filter(username = username).exists():
        print("not username")
        return JsonResponse({'status':'failure','message':'Invalid Username'},status = 400)
    
    # Get user data
    user = customer.objects.get(username=username)
    print(f"User found: {user.username}")
    
    # Construct the path to the user's profile image
    user_image_path = Path(settings.BASE_DIR) / 'assets' / str(user.profile_image.name)
    print(f"User profile image path: {user_image_path}")
    
    # Check if the user's profile image exists
    # if not user_image_path.exists():
    #     return JsonResponse({'status': 'failure', 'message': 'User profile image not found'}, status=404)
    
    # Save the camera image
    image_file_camera = request.FILES['image']
    print(f"Uploaded image: {image_file_camera.name}")
    print(f"Uploaded image size: {image_file_camera.size} bytes")

    try:
        image_data = image_file_camera.read()
        print(f"Image data read successfully. Size: {len(image_data)} bytes")
    except Exception as e:
        print(f"Error reading image data: {str(e)}")
        return JsonResponse({'status': 'failure', 'message': 'Error reading the uploaded image'}, status=500)

    # Debug: Check the image being saved
    print(f"Saving image: {image_file_camera.name}, Size: {len(image_data)} bytes")

    # Create a timestamp for the filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_extension = os.path.splitext(image_file_camera.name)[1]
    file_name = f"viewer_img_{timestamp}{file_extension}"

    # Construct the directory path to save the uploaded image
    media_dir = Path(settings.BASE_DIR) / 'assets' / 'images' / 'viewer_pic' / 'facecheckimg'
    media_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

    # Construct the full file path to save the uploaded image
    file_path = media_dir / file_name
    print(f"Saving image to: {file_path}")

    # Write the image data to the file
    with open(file_path, 'wb') as destination_file:
        destination_file.write(image_data)
        print(f"Image saved successfully at {file_path}")
    
    # Load the uploaded image for face recognition
    try:
        uploaded_image = face_recognition.load_image_file(file_path)
        uploaded_face_encoding = face_recognition.face_encodings(uploaded_image)
        
        if not uploaded_face_encoding:
            return JsonResponse({'status': "failure", 'message': "No face found in the uploaded image"}, status=400)
        
        uploaded_face_encoding = uploaded_face_encoding[0]
        print(f"Face encoding from uploaded image: {uploaded_face_encoding}")
    
    except Exception as e:
        return JsonResponse({'status': 'failure', 'message': f"Error loading image for face recognition: {str(e)}"}, status=400)
    
    # Process user image for face recognition
    try:
        user_image = face_recognition.load_image_file(user_image_path)
        face_encodings = face_recognition.face_encodings(user_image)
        if not face_encodings:
            print(f"No face found in user's profile image: {user_image_path}")
            return JsonResponse({"status": "failure", "message": "No face found in the user's profile image"}, status=400)
        user_face_encoding = face_encodings[0]
        print(f"Face encoding from user's profile image: {user_face_encoding}")
    except Exception as e:
        print(f"Error processing user profile image: {str(e)}")
        return JsonResponse({"status": "failure", "message": f"Error processing user profile image: {str(e)}"}, status=400)

    # Compare the face encodings
    results = face_recognition.compare_faces([user_face_encoding], uploaded_face_encoding)

    # Convert np.True_ to a plain True
    try:
        # Compare the face encodings
        results = face_recognition.compare_faces([user_face_encoding], uploaded_face_encoding)
        print(f"Comparison result: {results[0]}")

        if results[0]:
            request.session['user_id'] = user.pk
            request.session['user_email'] = user.email
            messages.success(request, "Login successful!")
            return JsonResponse({"status": "success", "message": "Face match found", 'redirect_url': '/customer/custadmin'}, status=200)
        else:
            return JsonResponse({'status': 'failure', 'message': 'Face match not found'}, status=400)

    except Exception as e:
        print(f"Error during face comparison: {str(e)}")
        return JsonResponse({"status": "failure", "message": "Error during login process"}, status=500)


def cust_logout(request): 
    request.session.flush()  
    messages.success(request,"Logged out Successfully")
    return HttpResponseRedirect('/')
       
        
def cust_forgetPass(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        if 'submit' in request.POST and request.POST['submit'] == 'send':
            print("send",email)
            if email is not None:
                orgnizer=customer.objects.filter(email = email)
                if orgnizer.exists():
                    org = customer.objects.get(email=email)
                    
                    subject = "Welcome to Django Wdding PLanner Pro...!!"
                    message = "Hello"+ org.full_name + "!! \n"+ "Thank you for visiting our website \n Thanking You..! Please open Mail to verify your email address..!"
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [org.email]
                    send_mail(subject , message , from_email ,to_list ,fail_silently=True)
                    
                    print("pk=",org)
                
                    context = {"org":org}
                    return render(request,"cust_forgetPass.html",context)
                else:
                    messages.success(request, "Email does not Exsist")
                    return HttpResponseRedirect("/host/host_forgetPass")
                    
        elif 'submit' in request.POST and request.POST['submit'] == 'Reset':
                print("reset")
                if request.method == "POST":
                    new_email = request.POST.get('email')
                    new_pass =request.POST.get('password')
                    cpass = request.POST.get('cpassword')
                    print(email,new_pass,cpass)
                        
                    if email is not None:
                     # Update the password
                        if customer.objects.filter(email=new_email).exists():
                            org= customer.objects.get(email=new_email)
                            if new_pass == cpass:
                                org.password = new_pass
                                org.save()
                            else:
                                messages.error(request,"Password does not match")
                                return HttpResponseRedirect("/customer/cust_forgetPass")
                        else:
                            messages.error(request,"Email is does not exists")
                            return HttpResponseRedirect("/customer/cust_forgetPass")
                        
                        messages.success(request, "Password is updated successfully")
                        return HttpResponseRedirect("/customer/cust_forgetPass")
                    else:
                            messages.error(request, "Email is required for the Change Password.")
                            return HttpResponseRedirect(request.path_info)
    return render(request,"cust_forgetPass.html")
  

        

    
        


