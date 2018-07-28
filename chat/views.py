from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from chat.models import Message,Record,Online_User
from chat.serializers import MessageSerializer, UserSerializer
from PIL import Image
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import os
from PIL import ImageTk
from friendship.models import Friend
import base64
import json
import cv2
import sqlite3
import numpy as np
import sqlite3
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver    
import datetime
import time
from django.shortcuts import render, get_object_or_404, redirect
import tkinter 
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from Profile.models import Profile
def online(request):
    re_id= request.POST['identity']
    t=Online_User.objects.filter(user_id=re_id).update(status=1)
def offline(request):
    re_id= request.POST['identity']
    t=Online_User.objects.filter(user_id=re_id).update(status=0)

def listcontacts(request):
    contactname=request.POST['name']
    contacts=User.objects.filter(username__startswith=contactname).values('username','id')
    print(contacts)
    # contacts=json.dumps(contacts
    # contacts=json.loads(contacts)
    return JsonResponse(list(contacts),safe=False)
def cryptograph(request):
    if request.method=='POST':
        key= Fernet.generate_key()
        f=Fernet(key)
        print(f)
        message=request.POST['message']
        message=message.encode('utf-8')
        token= f.encrypt(message)
        token=token.decode('utf-8')
        key=key.decode('utf-8')

        # dataa=({'token':token,'f':f})
        # print(dataa)
        # dataa= dataa.dumps(data)
        # datas=dataa.loads(data)
        # dating=json.loads(datas)
        # print(dating)
        return JsonResponse({'token':token,'key':key})


# @login_required
# def index(request):
#     return redirect('chats')

def index(request): 
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return redirect('login')
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

        else:
            return HttpResponse('{"error": "User does not exist"}')
        # a=User.objects.filter(id=request.user.id).update(last_login=datetime.datetime.now())
        # a.save()

        return redirect('chats')


@csrf_exempt
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
 
 
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# @receiver(user_logged_in)
# def got_online(sender, user, request, **kwargs):    
#     user.online.is_online = True
#     user.online.save()


# @receiver(user_logged_out)
# def got_offline(sender, user, request, **kwargs):   
#     user.online.is_online = False
#     user.online.save()


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def message_lists(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages =(Message.objects.filter(sender_id=sender, receiver_id=receiver)|Message.objects.filter(sender_id=receiver, receiver_id=sender)).last()
        serializer = MessageSerializer(messages,context={'request': request})
        return JsonResponse(serializer.data,safe=False)

def final(request):
    return render(request,"chat/final.html")

def register_view(request):
    """
    Render registration template
    """
    if request.user.is_authenticated:
        return redirect('chats')
    return render(request, 'chat/register.html', {})


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        t=Online_User.objects.filter(user_id=request.user.id).update(status=1,session_time=datetime.datetime.now())
        mess=[]
        use=User.objects.exclude(id=request.user.id)
        usering= {'use':use}
        a=0
        for b in usering['use']:
            i= usering['use'][a].id
            Me=(Message.objects.filter(sender_id=request.user.id, receiver_id=i)|Message.objects.filter(sender_id=i, receiver_id=request.user.id)).values().last()
            a=a+1
            mess.append(Me)
        friendsent= Friend.objects.filter(to_user_id=request.user.id) 
        # friendreceive= Friend.objects.filter(to_user_id=request.user.id)
       
        print(friendsent)
        # print(friendreceive)
        profile_pics=[]
        online_friends=[]
        friendlist=[]
        for friend in friendsent:
           friendname= User.objects.filter(id=friend.from_user_id).values('username','id')[0]
           profile_pic=Profile.objects.filter(user_id=friend.from_user_id).values('profile_pic')[0]
           online_friend= Online_User.objects.filter(user_id=friend.from_user_id).values('status','session_time')[0]
           friendlist.append(friendname)
           online_friends.append(online_friend)
           profile_pics.append(profile_pic)
        print("IT is all about friends")
        print(friendlist)
        print(profile_pics)
        print(online_friends)
        for i in friendlist:
            print(i['username'])
        for h in online_friends:
            print(h['session_time'])
            g= timezone.now()-h['session_time']
            if h['status'] =='1':
                if g.days > 0 or g.seconds >300:
                    h['status'] = '0'
                


        z=zip(use,mess)
        y=zip(friendlist,online_friends,profile_pics)
        print(y)
        fre = Friend.objects.requests(request.user)
        return render(request, 'chat/final.html',
                     {'users':z,'online_friend':y,'f_r_r':fre,'legal':Record.objects.filter(user_id=request.user.id), 'friends':friendlist })

        # return render(request, 'chat/chat.html',
        #               {'users': User.objects.exclude(username=request.user.username),'legal':Record.objects.filter(user_id=request.user.id)})


# def message_view(request, sender, receiver):
#     if not request.user.is_authenticated:
#         return redirect('index')
#     if request.method == "GET":
#         mess=[]
#         use=User.objects.exclude(id=request.user.id)
#         usering= {'use':use}
#         a=0
#         for b in usering['use']:
#             i= usering['use'][a].id
#             Me=Message.objects.filter(sender_id=request.user.id, receiver_id=i).values().last()
#             a=a+1
#             mess.append(Me)
#         z=zip(use,mess)
#         friendsent= Friend.objects.filter(from_user_id=request.user.id) 
#         # friendreceive= Friend.objects.filter(to_user_id=request.user.id)
#         print(friendsent)
#         # print(friendreceive)
#         friendlist=[]
#         for friend in friendsent:
#            friendname= User.objects.filter(id=friend.to_user_id).values('username','id')[0]
#            friendlist.append(friendname)
#         print("IT is all about friends")
#         print(friendlist)
#         return render(request, "chat/message.html",
#                       {'users':z,
#                        'receiver': User.objects.get(id=receiver),
#                        'legal':Record.objects.filter(user_id=request.user.id),
#                        'friends':friendlist,
#                        'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
#                                    Message.objects.filter(sender_id=receiver, receiver_id=sender)})


def message_view(request,receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        t=Online_User.objects.filter(user_id=request.user.id).update(status=1,session_time=datetime.datetime.now())
        mess=[]
        use=User.objects.exclude(id=request.user.id)
        usering= {'use':use}
        a=0
        for b in usering['use']:
            i= usering['use'][a].id
            Me=Message.objects.filter(sender_id=request.user.id, receiver_id=i).values().last()
            a=a+1
            mess.append(Me)
        z=zip(use,mess)
        friendsent= Friend.objects.filter(to_user_id=request.user.id) 
        # friendreceive= Friend.objects.filter(to_user_id=request.user.id)
        print(friendsent)
        # print(friendreceive)
        profile_pics=[]
        online_friends=[]
        friendlist=[]
        for friend in friendsent:
           friendname= User.objects.filter(id=friend.from_user_id).values('username','id')[0]
           profile_pic=Profile.objects.filter(user_id=friend.from_user_id).values('profile_pic')[0]
           online_friend= Online_User.objects.filter(user_id=friend.from_user_id).values('status','session_time')[0]
           friendlist.append(friendname)
           online_friends.append(online_friend)
           profile_pics.append(profile_pic)
       
        for i in friendlist:
            print(i['username'])
        for h in online_friends:
            print(h['session_time'])
            g= timezone.now()-h['session_time']
            if h['status'] =='1':
                if g.days > 0 or g.seconds >300:
                    h['status'] = '0'
        y=zip(friendlist,online_friends,profile_pics)
        fre = Friend.objects.requests(request.user)
        return render(request, "chat/message.html",
                      {'users':z,'f_r_r':fre,'online_friend':y,
                       'receiver': User.objects.get(id=receiver),
                       'legal':Record.objects.filter(user_id=request.user.id),
                       'friends':friendlist,
                       'messages': Message.objects.filter(sender_id=request.user.id, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=request.user.id)})

@csrf_exempt
def message_receive(request,sender=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        use= User.objects.exclude(id=request.user.id)
        usering= {'use':use}
        a=0
        for b in usering['use']:
            i=usering['use'][a].id
            messages =Message.objects.filter(sender_id=i, receiver_id=sender,is_read=False).last()
            a=a+1
            serializer = MessageSerializer(messages,context={'request': request})
            unwant=json.dumps(serializer.data)
            unwant=json.loads(unwant)
            if unwant['message']!= '':
                # messages.update(is_read=True)
                # messages.save()
                unwant.update({'sender_id':i})
                return JsonResponse(unwant)
        return HttpResponse(unwant)

def encode(request):
    if request.method == "POST":
        message = request.POST['message']
        length = len(message)
        userid= request.POST['receiver']
    # limit length of message to 255
        path="C:/Users/Anonymous1/Downloads/New folder/DRF-Chat-master/Finals/static/first/"
        imagepathss=[f for f in os.listdir(path)]
        imagePaths=[os.path.join("static/first/",f) for f in os.listdir(path)]
        # src='first/shailesh.png'
        src=imagePaths[0];
        img=Image.open(src)
        if length > 255:
            print("text too long! (don't exeed 255 characters)")
            return False
        if img.mode != 'RGB':
            print("image mode needs to be RGB")
            return False
    # use a copy of image to hide the text in
        encoded = img.copy()
        width, height = img.size
        index = 0
        result = []
        for d in message:
            bits = bin(ord(d))[2:]
            bits = '00000000'[len(bits):] + bits
            result.extend([int(bi) for bi in bits])
        print(result)
        s = "".join(chr(int("".join(map(str,result[i:i+8])),2)) for i in range(0,len(result),8))
        print(s)
        for row in range(height):
            for col in range(width):

                try:
                    r, g, b = img.getpixel((col, row))
                except ValueError:

                    r, g, b, a = img.getpixel((col, row))    
               
                if row == 0 and col == 0 :
                    asc = length
                    length=length*8
                    print(asc)
                elif row==0 and col == 1:
                    asc=userid
                    print(asc)
                elif index <=(length+1):
                    asc=set_bit(b,0,result[index-2])
                    print(result[index-2])
                    print(asc)
                else:
                    asc = b
                encoded.putpixel((col, row), (r, g , int(asc)))
                index += 1
        print(src)
        enco="enc_"+imagepathss[0]
        encoded_image = "./static/second/"+ enco
        # encoded_image_file = "first"+encoded_image
        encoded.save(encoded_image)
        os.remove(imagePaths[0])
        # with open(encoded_image_file, "rb") as imageFile:
        #     stri = base64.b64encode(imageFile.read())
        #     print(stri)     
        # d=json.loads(stri) 
        # print(d)
        # Image.open(encoded_image_file)
        # d= {'ima':encoded_image}
        # return JsonResponse(d)

        return HttpResponse(enco)

   #image2 = Image.open(encoded_image_file)
    



def set_bit(v, index, x):    
    """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""                           
    mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
    v &= ~mask          # Clear the bit indicated by the mask (if x is False)
    if x:          
        v |= mask
    return v

# def getprofile(Id):
#         conn=sqlite3.connect("newfacebase.db")
#         print(Id)
#         cursor=conn.execute("SELECT ID,Name FROM Peoples WHERE ID="+str(Id))
#         profile=None
#         for row in cursor:
#             print(row)
#             profile=row
#         conn.commit()
#         conn.close()
#         return profile

def getprofile(Id):

        cursor= User.objects.filter(id=Id).values_list()
        print(cursor)
        if not cursor:
            profile=None
        else:
            profile=cursor
        return profile



# def insert(Id,Names):
#         sa= train(id1=Id,name=Names)
#         sa.save()

def addimage(request):
    root=tkinter.Tk()
    Id1=request.POST['id1']
    labeld= tkinter.Button(root,text="Click Here",command=lambda:addimages(Id1),bg="green")
    labeld.pack()
    root.lift()
    root.attributes('-topmost',True)
    root.after_idle(root.attributes,'-topmost',False)
    root.mainloop()
    root.destroy()

def addimages(Id1):    
    detector=cv2.CascadeClassifier('C:/Users/Anonymous1/Desktop/begin/first/haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0) 
    # destination="C:/Users/Anonymous1/Downloads/Compressed/DRF-Chat-master/DRF-Chat-master/firstdataSet"
    # os.chdir(destination) 
    
    # Id1=request.POST['id1']
    print("ID")
    print(Id1)
    sampleNum=0
    font = cv2.FONT_HERSHEY_SIMPLEX
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.2, 5)
        sa=10-sampleNum
        cv2.putText(img,str("Images remaining"+str(sa)),(2,50),font,0.55,(0,255,0),1)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(230,230,250),2)
            #incrementing sample number
        
        
            sampleNum=sampleNum+1   
            #saving the captured face in the dataset folder
            print(sampleNum)
            cv2.imwrite('C:/Users/Anonymous1/Downloads/New folder/DRF-Chat-master/Finals/dataSet/User.'+Id1+'.'+str(sampleNum)+'.jpg',gray[y:y+h,x:x+w])
            # cv2.imwrite('shailesh'+Id1+'.jpg',gray[y:y+h,x:x+w])

        cv2.imshow('frame',img)
        # os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
        if(cv2.waitKey(100)== ord('q')):
            break
        # break if the sample number is morethan 20
        elif sampleNum>10:
            break
    
    print("out of the loop")
    if sampleNum>10:
        added= Record.objects.filter(user_id=Id1).update(image_added=1)   
        print(added)
        imagetrain(Id1)
    print("OK I am inside imagetrain")
    cam.release()
    cv2.destroyAllWindows()
    
    return HttpResponse(sampleNum)
    #imagerecog.func3()
    

def decoded(request):
    sourc=request.POST['message']
    sour= os.path.basename(sourc)
    print("Sanjay")
    source= 'static/second/'+ sour
    print(source)
    value=imagerecognition(source)
    if value>5:        
        img=Image.open(source)
        width, height = img.size
        msg = []
        index = 0
        for row in range(height):        
            for col in range(width):                        
                try:                    
                    r, g, b = img.getpixel((col, row))
                except ValueError:
# need to add transparency a for some .png files
                    r, g, b, a = img.getpixel((col, row))       
# first pixel r value is length of message
                if row == 0 and col == 0 :                          
                    length = b
                    length=length*8
                    print(length)
                elif row==0 and col ==1 :
                    a=10
                    print(a)
                elif index<=length:                            
                    print(b)
                    by=b & 1                
                    print(by)
                    msg.extend([by])
                    index += 1
        s = "".join(chr(int("".join(map(str,msg[i:i+8])),2)) for i in range(0,len(msg),8))
        print(s)
        return HttpResponse(s)
    return HttpResponse("Image Recognition was not successful")


def imagerecognition(dname):    
    recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer.load('trainer/nttrainner.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceDetect = cv2.CascadeClassifier(cascadePath);
    img1=Image.open(dname)
    width,height=img1.size
    for row in range(height):
        for col in range(width):
            try:
               r, g, b = img1.getpixel((col, row))
            except ValueError:
               r, g, b, a = img1.getpixel((col, row))
               
            if row==0 and col == 1:
                print("Its bad")
                asc=b
    print("Sai ho")     
    print(asc)                  
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    value=0
    while True:
        ret, img =cam.read()
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray, 1.3,5)
        if  value>5:
            break
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            print(Id)
            print(conf)
            print("Sai ho")
            print(asc)
            profile=getprofile(Id)
            print(profile[0])
            if(profile == None):
                cv2.putText(img,str("Unknown"),(x,y+h),font,0.55,(0,255,0),1)            
            else:
                print('Sha')
                if conf<45:
                    cv2.putText(img,str(profile[0][0]),(x,y+h),font,0.55,(0,255,0),1)
                    cv2.putText(img,str(profile[0][4]),(x,y+h+30),font,0.55,(0,255,0),1)
                    if str(profile[0][0])==str(asc): 
                        value=value+1
                        print("Value is")
                        print(value)
                else:
                    cv2.putText(img,str("Unknown"),(x,y+h),font,0.55,(0,255,0),1)
                # if str(profile[0][0])==str(asc): 
                #     value=value+1
                #     print("Value is")
                #     print(value)
            
    
        cv2.imshow('Face recognizer',img) 
        if(cv2.waitKey(10)==ord('q')):
            break
        
    cam.release()
    cv2.destroyAllWindows()
    return value

    
def imagetrain(Id1):
    print("In image training ")
    print(Id1)
    recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer.load('C:/Users/Anonymous1/Downloads/New folder/DRF-Chat-master/Finals/trainer/nttrainner.yml')
    faces,IDs = getImagesWithID('C:/Users/Anonymous1/Downloads/New folder/DRF-Chat-master/Finals/dataSet',Id1)
    print(faces)
    print(IDs)
    recognizer.update(faces, np.array(IDs))
    recognizer.save('C:/Users/Anonymous1/Downloads/New folder/DRF-Chat-master/Finals/trainer/nttrainner.yml')
    cv2.destroyAllWindows()
    

def getImagesWithID(path,Id):
        #get the path of all the files in the folder
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
        print("User ID is")
        print(Id)
        
        print(imagePaths)
        #create empty face list
        del imagePaths[0]
        faces=[]
        #create empty ID list
        IDs=[]
        #now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            #loading the image and converting it to gray scale
            print(imagePath)
            faceImg=Image.open(imagePath).convert('L')
            #Now we are converting the PIL image into numpy array
            faceNp=np.array(faceImg,'uint8')
            #getting the Id from the image
            ID=int(os.path.split(imagePath)[-1].split(".")[1])
            print("ID is")
            print(ID)
            if ID == int(Id):
                faces.append(faceNp)
                IDs.append(ID)
                print(IDs)
                print(imagePath)
            
            #cv2.imshow("training",faceNp)
            #cv2.waitKey(10)
        return faces,IDs


# def deletemessage(request):
#     sid=request.POST['senderid']
#     rid=request.POST['receiverid']
#     delete=Message.objects.filter(sender_id= sid ,receiver_id=rid) | Message.objects.filter(sender_id= rid ,receiver_id=sid)
#     # deleted= delete.update[senderview="Notview"]
#     # return HttpResponse("Hello")
