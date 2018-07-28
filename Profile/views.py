from django.shortcuts import render
from .forms import ProfileForm
from django.shortcuts import redirect, render
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message,Record,Online_User
from chat.serializers import MessageSerializer, UserSerializer
from PIL import Image
import os
from PIL import ImageTk
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
from friendship.models import Friend
from cryptography.fernet import Fernet
from django.forms.models import model_to_dict
from django.utils import timezone

def ProfileUpdate(request):
	if request.method == 'POST':
		a=request.user.username
		b='/profile/'+a+'/'
		profileForm = ProfileForm(request.POST, request.FILES, instance = request.user.profile)

		if profileForm.is_valid():
			profileForm.save()
			return redirect('b')
	else:
		profileForm = ProfileForm(instance=request.user.profile)

	return render(request, 'profile/profileEdit.html', {
		'profileForm': profileForm,
	})



def view_profile(request,sender=None):
	t=Online_User.objects.filter(user_id=request.user.id).update(status=1,session_time=datetime.datetime.now())
	mess=[]
	use=User.objects.exclude(id=request.user.id)
	usering= {'use':use}
	a=0
	print(sender)
	listing= User.objects.get(username=sender)
	for b in usering['use']:
	    i= usering['use'][a].id
	    Me=(Message.objects.filter(sender_id=request.user.id, receiver_id=i)|Message.objects.filter(sender_id=i, receiver_id=request.user.id)).values().last()
	    a=a+1
	    mess.append(Me)
	friendsent= Friend.objects.filter(to_user_id=request.user.id) 
	    # friendreceive= Friend.objects.filter(to_user_id=request.user.id)
	print(friendsent)
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
	print(sender)
	print(friendlist)
	for h in online_friends:
		print(h['session_time'])
		g= timezone.now()-h['session_time']
		if h['status'] =='1':
			if g.days > 0 or g.seconds >300:
				h['status'] = '0'


  
	senderid= User.objects.filter(username=sender).values_list('id')[0]
	asafriend= Friend.objects.filter(from_user_id=senderid[0],to_user_id=request.user.id).values_list() | Friend.objects.filter(from_user_id=request.user.id,to_user_id=senderid[0]).values_list()
	    # for i in friendlist:
	    #     print(i[0]['username'])
	print("As a friend")
	print(senderid[0])
	print(asafriend)
	x=zip(friendlist,online_friends,profile_pics)
	y=[]
	if len(asafriend)==0:
		y.append(0);
	else:
		y.append(1);
	print("Y:")
	print(y)
	z=zip(use,mess)
	print(listing)
	return render(request, 'profile/profile.html',
	                 {'asafriend':y,'users':z,'online_friend':x,'userr':listing,'legal':Record.objects.filter(user_id=request.user.id), 'friends':friendlist })
