from django.urls import path
from .views import ProfileUpdate
from .views import view_profile


urlpatterns = [
	path('editProfile', ProfileUpdate, name = 'editProfile'),
	# path('profile/',view_profile,name='view_profile'),
	path('profile/<str:sender>/',view_profile,name='view_profile'),
	
]