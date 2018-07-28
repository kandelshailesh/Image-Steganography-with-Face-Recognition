from django.urls import path
from django.contrib.auth import views as auth_views
from register import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('password/', views.change_password, name='change_password'),
   
]
