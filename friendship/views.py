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
from django.utils import timezone

try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User

from django.shortcuts import render, get_object_or_404, redirect

from friendship.exceptions import AlreadyExistsError
from friendship.models import Friend, Follow, FriendshipRequest, Block

get_friendship_context_object_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_NAME', 'user')
get_friendship_context_object_list_name = lambda: getattr(settings, 'FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME', 'users')


def view_friends(request, username, template_name='friendship/friend/user_list.html'):
    """ View the friends of a user """
    user = get_object_or_404(user_model, username=username)
    qs = Friend.objects.select_related('from_user', 'to_user').filter(to_user=user).all()
    friends = [u.from_user for u in qs]
    # friends = Friend.objects.friends(user)
    fr = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(from_user=user).all()
    frr = [u.to_user for u in fr]
    fs = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(to_user=user).all()
    fsr = [u.from_user for u in fs]
    usr = user_model.objects.exclude(username=username)
    fre = Friend.objects.requests(request.user)
    fse = Friend.objects.sent_requests(request.user)
    args = {'users': usr, 'friends': friends, 'f_r_r': fre, 'f_s_r': fse, 'frr': frr,'fsr':fsr}
    return render(request, template_name, args)


def test_view_friends(request):
    """ View the friends of a user """
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
    
    online_friends=[]
        # print(friendreceive)
    friendlist=[]
    for friend in friendsent:
        friendname= User.objects.filter(id=friend.from_user_id).values('username','id')[0]
        profile_pic=Profile.objects.filter(user_id=friend.from_user_id).values('profile_pic')[0]
        profile_pics.append(profile_pic)
        online_friend= Online_User.objects.filter(user_id=friend.from_user_id).values('status','session_time')[0]
        friendlist.append(friendname)
        online_friends.append(online_friend)
    print("IT is all about friends")
    print(friendlist)
    for i in friendlist:
            print(i['username'])
    for h in online_friends:
        print(h['session_time'])
        g= timezone.now()-h['session_time']
        if h['status'] =='1':
            if g.days > 0 or g.seconds >300:
                h['status'] = '0'
    y=zip(friendlist,online_friends,profile_pics)
        # for i in friendlist:
        #     print(i[0]['username'])
    z=zip(use,mess)
    user = get_object_or_404(user_model, username=request.user)
    qs = Friend.objects.select_related('from_user', 'to_user').filter(to_user=user).all()
    friends = [u.from_user for u in qs]
    # friends = Friend.objects.friends(user)
    fsentf = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(from_user=user).all()
    fsentu = [u.to_user for u in fsentf]
    frecf=FriendshipRequest.objects.select_related('from_user','to_user').filter(to_user=user).all()
    frecu=[u.from_user for u in frecf]
    usr = user_model.objects.exclude(username=request.user)
    fre = Friend.objects.requests(request.user)
    fse = Friend.objects.sent_requests(request.user)
    args = {'usering': usr, 'friends': friends,'online_friend':y, 'f_r_r': fre, 'f_s_r': fse, 'fsentu': fsentu,'frecu':frecu,'users':z,'legal':Record.objects.filter(user_id=request.user.id), 'friends':friendlist}
    if request.is_ajax():
        # html = render_to_string('friendship/friend/testfirst.html', args)
        html = render_to_string('friendship/friend/test.html', args)
        return HttpResponse(html)
    return render(request, 'friendship/friend/test.html' , args)


@login_required
def friendship_add_friend(request, to_username, template_name='friendship/friend/add.html'):
    """ Create a FriendshipRequest """
    ctx = {'to_username': to_username}
    if request.method != 'POST':
        to_user = user_model.objects.get(username=to_username)
        from_user = request.user
        try:
            Friend.objects.add_friend(from_user, to_user)
        except AlreadyExistsError as e:
            ctx['errors'] = ["%s" % e]
        else:
            return redirect('test_friendship_view_friends')

    return render(request, template_name, ctx)


@login_required
def friendship_remove_friend(request, to_username):
    to_user = user_model.objects.get(username=to_username)
    Friend.objects.remove_friend(request.user, to_user)
    return redirect('test_friendship_view_friends')


@login_required
def friendship_accept(request, friendship_request_id):
    """ Accept a friendship request """
    if request.method != 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_received,
            id=friendship_request_id)
        f_request.accept()
        return redirect('test_friendship_view_friends')

    return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)


@login_required
def friendship_reject(request, friendship_request_id):
    """ Reject a friendship request """
    if request.method != 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_received,
            id=friendship_request_id)
        # reject garda rahirakhyo....rejected ma date vara basdo raixa...
        # f_request.reject()
        f_request.cancel()
        return redirect('test_friendship_view_friends')

    return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)


@login_required
def friendship_cancel(request, friendship_request_id):
    """ Cancel a previously created friendship_request_id """
    if request.method != 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_sent,
            id=friendship_request_id)
        f_request.cancel()
        return redirect('test_friendship_view_friends')

    return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)


@login_required
def friendship_request_list(request, template_name='friendship/friend/requests_list.html'):
    """ View unread and read friendship requests """
    friendship_requests = Friend.objects.requests(request.user)
    # equivalent two lines below
    # ff = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(to_user=request.user,rejected__isnull=True).all()
    # friendship_requests = list(ff)

    # friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)
    return render(request, template_name, {'requests': friendship_requests})


@login_required
def friendship_request_list_rejected(request, template_name='friendship/friend/requests_list.html'):
    """ View rejected friendship requests """
    # friendship_requests = Friend.objects.rejected_requests(request.user)
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)

    return render(request, template_name, {'requests': friendship_requests})


@login_required
def friendship_requests_detail(request, friendship_request_id, template_name='friendship/friend/request.html'):
    """ View a particular friendship request """
    f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)

    return render(request, template_name, {'friendship_request': f_request})


# def followers(request, username, template_name='friendship/follow/followers_list.html'):
#     """ List this user's followers """
#     user = get_object_or_404(user_model, username=username)
#     followers = Follow.objects.followers(user)

#     return render(request, template_name, {
#         get_friendship_context_object_name(): user,
#         'friendship_context_object_name': get_friendship_context_object_name()
#     })


# def following(request, username, template_name='friendship/follow/following_list.html'):
#     """ List who this user follows """
#     user = get_object_or_404(user_model, username=username)
#     following = Follow.objects.following(user)

#     return render(request, template_name, {
#         get_friendship_context_object_name(): user,
#         'friendship_context_object_name': get_friendship_context_object_name()
#     })


# @login_required
# def follower_add(request, followee_username, template_name='friendship/follow/add.html'):
#     """ Create a following relationship """
#     ctx = {'followee_username': followee_username}

#     if request.method == 'POST':
#         followee = user_model.objects.get(username=followee_username)
#         follower = request.user
#         try:
#             Follow.objects.add_follower(follower, followee)
#         except AlreadyExistsError as e:
#             ctx['errors'] = ["%s" % e]
#         else:
#             return redirect('friendship_following', username=follower.username)

#     return render(request, template_name, ctx)


# @login_required
# def follower_remove(request, followee_username, template_name='friendship/follow/remove.html'):
#     """ Remove a following relationship """
#     if request.method == 'POST':
#         followee = user_model.objects.get(username=followee_username)
#         follower = request.user
#         Follow.objects.remove_follower(follower, followee)
#         return redirect('friendship_following', username=follower.username)

#     return render(request, template_name, {'followee_username': followee_username})


def all_users(request, template_name="friendship/user_actions.html"):
    users = user_model.objects.all()

    return render(request, template_name, {get_friendship_context_object_list_name(): users})


# def blocking(request, username, template_name='friendship/block/blockers_list.html'):
#     """ List this user's followers """
#     user = get_object_or_404(user_model, username=username)
#     blockers = Block.objects.blocked(user)

#     return render(request, template_name, {
#         get_friendship_context_object_name(): user,
#         'friendship_context_object_name': get_friendship_context_object_name()
#     })


# def blockers(request, username, template_name='friendship/block/blocking_list.html'):
#     """ List who this user follows """
#     user = get_object_or_404(user_model, username=username)
#     blocking = Block.objects.blocking(user)

#     return render(request, template_name, {
#         get_friendship_context_object_name(): user,
#         'friendship_context_object_name': get_friendship_context_object_name()
#     })


# @login_required
# def block_add(request, blocked_username, template_name='friendship/block/add.html'):
#     """ Create a following relationship """
#     ctx = {'blocked_username': blocked_username}

#     if request.method == 'POST':
#         blocked = user_model.objects.get(username=blocked_username)
#         blocker = request.user
#         try:
#             Block.objects.add_block(blocker, blocked)
#         except AlreadyExistsError as e:
#             ctx['errors'] = ["%s" % e]
#         else:
#             return redirect('friendship_blocking', username=blocker.username)

#     return render(request, template_name, ctx)


# @login_required
# def block_remove(request, blocked_username, template_name='friendship/block/remove.html'):
#     """ Remove a following relationship """
#     if request.method == 'POST':
#         blocked = user_model.objects.get(username=blocked_username)
#         blocker = request.user
#         Block.objects.remove_block(blocker, blocked)
#         return redirect('friendship_blocking', username=blocker.username)

#     return render(request, template_name, {'blocked_username': blocked_username})
