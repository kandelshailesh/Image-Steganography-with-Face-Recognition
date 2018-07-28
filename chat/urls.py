from django.contrib.auth.views import logout
from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    # path('',views.final,name='final'),
    path('', views.index, name='index'),
    path('chat', views.chat_view, name='chats'),
    # path('chat/<int:sender>/<int:receiver>', views.message_view, name='chat'),
    path('chat/<int:receiver>',views.message_view,name='chat'),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('apis/messages/<int:sender>/<int:receiver>', views.message_lists, name='message-details'),
    path('apis/messages/<int:sender>',views.message_receive,name='message-receive'),
    path('api/messages', views.message_list, name='message-list'),
    path('api/users/<int:pk>', views.user_list, name='user-detail'),
    path('api/users', views.user_list, name='user-list'),
    path('logout', logout, {'next_page': 'index'}, name='logout'),
    path('register', views.register_view, name='register'),
    path('encode',views.encode,name='encode'),
    path('decoded',views.decoded,name='decoded'),
    path('addimage',views.addimage,name='addimage'),
    path('crypto',views.cryptograph,name='cryptography'),
    path('listcontacts',views.listcontacts,name='listcontacts'),
    path('online',views.online,name='online'),
    path('offline',views.offline,name='offline'),
    
    # path('delete',views.deletemessage,name='deletemessage'),
]
