from django.shortcuts import render
from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib import messages
from myapp.models import User_master
import face_recognition
import cv2
import os
from django.conf import settings
from .models import *
from django.shortcuts import render,redirect
import threading
import time,datetime

# session
from .models import ViewerSession
from .forms import ViewerSessionForm

def home(request):
    return render(request, "home.html", {'uid': "user"})
    

def userhome(request):
    user_id = request.session.get('user_id')
    print(request.session.get('user_id'))
    context = {}  # Initialize context dictionary

    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/')

    # Retrieve the user object based on the user_id stored in the session
    user = User_master.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
         # Start the periodic task
        # periodic_task.delay(user_id)
        # output = load_img(user)
        # # output =  start_periodic_task(user)
        # print("outpu:t:",output)
        # result = "Unkown Person"
        # status = "Not Marked"
        
        # if  output and output is not None:
        #     result = "Successful"
        #     status = "Marked"
        
        #     # return redirect('/userhome')
        #     return render(request, "home.html", {'uid': user})
        # else:
        #     request.session.flush()
        #     return redirect('/userhome')
        print("userhome###########$$$$$$$$$")
        return render(request, "home.html", {'uid': user})
    else:
        # User does not exist, handle accordingly (redirect, show error, etc.)
        messages.error(request, "User not found.")
        return redirect('/')
  
def load_img(user):
    base_dir = str(settings.BASE_DIR)
    list_of_image = []
    list_of_id = []
    userprofile = User_master.objects.filter()
    for i in userprofile:
        # list_of_image.append(base_dir+i.image.url)
        list_of_image.append(base_dir+"\\static\\assets\\img\\viewer_pic\\" +i.user_profile_image)
        list_of_id.append(i.viewer_id)
    list_of_image_person = []


    for i in list_of_image:
        image_of_person = face_recognition.load_image_file(i)
        list_of_image_person.append(image_of_person)
    return encoding_faces(user,list_of_image_person,list_of_id)
    
def encoding_faces(user,list_of_image,list_of_id):
    list_of_face_encoding = []
    for i in list_of_image:
        encodings = face_recognition.face_encodings(i)
        
        if encodings:
            list_of_face_encoding.append(encodings[0])
        else:
            print("no face")
        
    return recognize_faces(user,list_of_face_encoding,list_of_id)

def recognize_faces(user,list_of_face_encoding,list_of_id = None):
    file_path = open_ca(user)
    unkown  = face_recognition.load_image_file(file_path)
    # print(unkown)
    try:
        face_encoding_UN = face_recognition.face_encodings(unkown)
        if not face_encoding_UN:
            print("face_encoding_UN not detected")
            return False
        
        unknown_fc = face_encoding_UN[0]
        results = face_recognition.compare_faces(list_of_face_encoding,unknown_fc)
        
        userprofile = User_master.objects.get(viewer_id = user.viewer_id)
        index = list_of_id.index(userprofile.viewer_id)
        
        
        # print(results,index,"sjfhdjs" ,file_path)
        if results[index]:
            print("match")
            return True
        else:
            print("unknown")
            return False
    except:
        return False

def open_ca(user):
    # Open video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open video capture")
    
    # Read frame from video capture
    ret, frame = cap.read()
    if not ret:
        raise Exception("Could not read frame")
    
    
    # Generate file path
    file_path = check(user)
    
    # Ensure directory exists
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create directory if it doesn't exist
    
    # Save the frame to the file
    if not cv2.imwrite(file_path, frame):
        raise Exception(f"Could not write image to {file_path}")
    # else:
    #     cv2.imwrite(file_path,frame)
    # Release video capture and close windows
    cap.release()
    cv2.destroyAllWindows()
    return file_path

def check(user):
    base_dir = str(settings.BASE_DIR)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Construct the file path
    # media_dir = os.path.join(settings.BASE_DIR, 'static', 'assets', 'img', 'viewer_pic')
    media_dir = base_dir + "\\static\\assets\\img\\viewer_pic\\facecheckimg\\viewer_img_" 
    
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)  # Ensure the directory exists
    else:pass
        # print(f"Directory{media_dir} created success")
        
    # file_path = media_dir + "/img.jpeg"
    file_path = media_dir + str(timestamp) + ".jpeg"
    # file_path = os.path.join(media_dir, 'image.jpeg')  # Ensure you use a valid extension
    # print(file_path,"####")
    return file_path


def user_login(request):
    # if request.method == "POST":
    #     username1=request.POST.get('username')
    #     password1= request.POST.get('password')
    #     if 'submit' in request.POST and request.POST['submit'] == 'face Login':
    #         if username1 is None or password1 is None or username1 == '' or password1 == '':
    #             messages.error(request,"Please Enter Username and Password")
    #         else:
    #             if not User_master.objects.filter(username=username1).exists():
    #                 print("bad")
    #                 messages.error(request,"Invalid Username ")
    #                 return redirect('/') 
                
    #             usern = User_master.objects.filter(username=username1).exists()
    #             if usern == True:
    #                 user= User_master.objects.get(username=username1)
                    
    #                 if user.password == password1:
    #                     request.session['user_id'] = user.pk
    #                     request.session['user_email'] = user.email
    #                     print("login")
    #                     id = int(user.viewer_id)
    #                     return redirect(f"/userhome")
    #                 else:
    #                     messages.error(request,"Wronge Password.")

    return render(request,"login.html")

def face_login(request, username):
    print("faceLogin", username)
    if request.method == 'POST':
        # session
        form = ViewerSessionForm(request.POST)
        if form.is_valid():
            viewer_session = form.save(commit=False)
            viewer_session.viewer = request.user
            viewer_session.save()
            return redirect('viewer_session_list')
        else:
            form = ViewerSessionForm()
        
        
        if not request.FILES.get('image'):
            return JsonResponse({'status': 'failure', 'message': 'Image is required'}, status=400)

        if not username or not User_master.objects.filter(username=username).exists():
            return JsonResponse({'status': 'failure', 'message': 'Invalid Username'}, status=400)

        user = User_master.objects.get(username=username)
        user_image_path = os.path.join(settings.BASE_DIR, 'static', 'assets', 'img', 'viewer_pic', user.user_profile_image)

        # Save camera image
        image_file_camera = request.FILES['image']
        # Read the image data
        image_data = image_file_camera.read()

        # Create a timestamp for the filename
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_extension = os.path.splitext(image_file_camera.name)[1]  # Get the file extension
        file_name = f"viewer_img_{timestamp}{file_extension}"
        # Construct the directory path
        media_dir = os.path.join(settings.BASE_DIR, 'static', 'assets', 'img', 'viewer_pic', 'facecheckimg')
        # Ensure the directory exists
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)
        # Construct the full file path
        file_path = os.path.join(media_dir, file_name)
        # Save the uploaded file
        with open(file_path, 'wb') as destination_file:
            destination_file.write(image_data)

        # Load the uploaded image for face recognition
        uploaded_image = face_recognition.load_image_file(file_path)
        uploaded_face_encoding = face_recognition.face_encodings(uploaded_image)

        if not uploaded_face_encoding:
            return JsonResponse({'status': 'failure', 'message': 'No faces found in the uploaded image'}, status=400)

        uploaded_face_encoding = uploaded_face_encoding[0]

        if os.path.exists(user_image_path):
            user_image = face_recognition.load_image_file(user_image_path)
            face_encodings = face_recognition.face_encodings(user_image)
            if face_encodings:
                user_face_encoding = face_encodings[0]
                results = face_recognition.compare_faces([user_face_encoding], uploaded_face_encoding)
                if results[0]:
                    request.session['user_id'] = user.pk
                    request.session['user_email'] = user.email
                    
                    # Create a new ViewerSession instance
                    viewer_session = ViewerSession(
                        session_id=file_name,
                        viewer=user,
                        joined_at=datetime.datetime.now()
                    )
                    viewer_session.save()
                    
                    messages.success(request,"login successfully...!")
                    return JsonResponse({'status': 'success', 'message': 'Face match found', 'redirect_url': '/userhome'}, status=200)

        return JsonResponse({'status': 'failure', 'message': 'No match found', 'form': form}, status=404)

    return JsonResponse({'status': 'failure', 'message': 'Invalid request method' ,'form': form }, status=405)
    



from multiprocessing import Queue
# result_queue = Queue
def run_periodic_task(user,result_queue,request):
    while True:
        output = load_img(user)
        result_queue.put(output)
        
        if not output:
            print("stop_tread",output)
            result_queue.put(output)
            break
            
        print(output,"I am in thread$$")
        time.sleep(30)# Sentinel value indicating the thread has stopped
          

def start_periodic_task(user,request):
    if user:
        result_queue = Queue()
        thread = threading.Thread(target = run_periodic_task, args=(user, result_queue,request))
        # print(thread,"#$%",result_queue.get())
        thread.daemon = True  # Ensure the thread exits when the main program exits
        thread.start()
        print(thread,"#$%")
        return thread, result_queue
    return None, None


def video(request):
    user_id = request.session.get('user_id')
    print(request.session.get('user_id'))
    context = {}  # Initialize context dictionary

    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/')

    # Retrieve the user object based on the user_id stored in the session
    user = User_master.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        thread, result_queue = start_periodic_task(user,request)
        # print("Periodic task started")
        
        # print("outpu:t:",result_queue.get())
        result_message = "Unknown Person"
        status = "Not Marked"
        # try:
            # Retrieve result from the queue
        result = result_queue.get() 
        print(result,"result")
        if result:
                result_message = "Successful"
                status = "Marked"
                messages.error(request,"face recognize...!")
                # return HttpResponseRedirect(request.path_info)
                
        else:
                print("false")
                messages.error(request,"Not face recognize...!")
                return HttpResponseRedirect(request.path_info)
                # request.session.flush()
                # return redirect("/")
        # except:
        #     print("false")
        #     request.session.flush()
        #     return redirect("/")
        
        context = {"uid": "love you Thar"}
        return render(request, "hi.html", context)


def opencJS(request):
    user_id = request.session.get('user_id')
    print(request.session.get('user_id'))
    context = {}  # Initialize context dictionary

    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/')

    # Retrieve the user object based on the user_id stored in the session
    user = User_master.objects.filter(pk=user_id).first()

    # Check if the user exists
    if user:
        print(user)
        
    return render(request,'opencJS.html')    

import os
import datetime
import io
from django.conf import settings
from django.http import JsonResponse
from PIL import Image
import face_recognition  # Replace with the actual face recognition library you use


def process_image(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/')

    # Retrieve the user object based on the user_id stored in the session
    user = User_master.objects.filter(pk=user_id).first()

    if not user:
        # User not found
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

    if request.method == 'POST' and request.FILES.get('image'):
        image_file_camera = request.FILES['image']
        
        # Read the image data
        image_data = image_file_camera.read()

        # Create a timestamp for the filename
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_extension = os.path.splitext(image_file_camera.name)[1]  # Get the file extension
        file_name = f"viewer_img_{timestamp}{file_extension}"

        # Construct the directory path
        media_dir = os.path.join(settings.BASE_DIR, 'static', 'assets', 'img', 'viewer_pic', 'facecheckimg')

        # Ensure the directory exists
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        # Construct the full file path
        file_path = os.path.join(media_dir, file_name)

        # Save the uploaded file
        with open(file_path, 'wb') as destination_file:
            destination_file.write(image_data)

        # Load the uploaded image for face recognition
        uploaded_image = face_recognition.load_image_file(file_path)
        uploaded_face_encoding = face_recognition.face_encodings(uploaded_image)

        if not uploaded_face_encoding:
            messages.error(request,"face not found")
            return JsonResponse({'status': 'failure', 'message': 'No faces found in the uploaded image'}, status=400)

        uploaded_face_encoding = uploaded_face_encoding[0]

        # Retrieve user images and perform face recognition
        list_of_face_encodings = []
        list_of_user_ids = []

        user_profiles = User_master.objects.all()
        for profile in user_profiles:
            user_image_path = os.path.join(settings.BASE_DIR, 'static', 'assets', 'img', 'viewer_pic', profile.user_profile_image)
            if os.path.exists(user_image_path):
                user_image = face_recognition.load_image_file(user_image_path)
                face_encodings = face_recognition.face_encodings(user_image)
                if face_encodings:
                    list_of_face_encodings.append(face_encodings[0])
                    list_of_user_ids.append(profile.viewer_id)

        # Recognize faces
        results = face_recognition.compare_faces(list_of_face_encodings, uploaded_face_encoding)

        if user.viewer_id in list_of_user_ids and results[list_of_user_ids.index(user.viewer_id)]:
            messages.success(request, "Face match")
            response_data = {'status': 'success', 'message': 'Face match found'}
            return JsonResponse(response_data, status=200)
        else:
            # messages.error(request, "face login again ")
            response_data = {'status': 'failure', 'message': 'Face login Again'}
            return JsonResponse(response_data, status=404)
    
    

def min10(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        # User is not logged in, redirect to login page
        return redirect('/')

    # Retrieve the user object based on the user_id stored in the session
    user = User_master.objects.filter(pk=user_id).first()

    if not user:
        print("10min")
        
    return render(request,'10min.html')
   
     
     
    #  Session Maintain
# views.py
from django.shortcuts import render, redirect


def create_viewer_session(request):
    if request.method == 'POST':
        form = ViewerSessionForm(request.POST)
        if form.is_valid():
            viewer_session = form.save(commit=False)
            viewer_session.viewer = request.user
            viewer_session.save()
            return redirect('viewer_session_list')
    else:
        form = ViewerSessionForm()
    return render(request, 'create_viewer_session.html', {'form': form}) 


def logout(request):
    logout = ViewerSession.objects.get(pk = request.session.get('user_id'))
    return HttpResponseRedirect()

def contact(request):
    return render(request,"contact.html")

def Deposit(request,service):
    if service == "cur":
        val = "current"
    elif service == "sav":
        val = "Saving"
    elif service == "fix":
        val ="fix"
    elif service == "mis":
        val ="mis"
    elif service == "DDS":
        val = "DDS"
    elif service == "RD":
        val = "RD"
    
    context = {"val":val}
    return render(request,"Deposit.html",context)

def Loan(request,loan):
    if loan == "Tw":
        val = "Tw"
    elif loan == "jil":
        val ="jil"
    elif loan == "DDLS":
        val ="DDLS"
    
    context = {"val":val}
    return render(request,"loan.html",context)

def careers(request):
    context = {"val":"val"}
    return render(request,"careers.html",context)

def otherser(request):
    return render(request,"otherSer.html")

