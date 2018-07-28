from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

default_profile='profile_images/shailesh.png'
default_cover='cover_images/kajal.png'

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True, default=True)
	bio = models.TextField(max_length=100, blank=True)
	location = models.CharField(max_length=50, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	STATUS = (
		('S', 'Single'),
		('R', 'In Relationship'),
		('E', 'Engaged'),
		('M', 'Married'),
	)

	maritial_status = models.CharField(max_length=50, choices=STATUS, default='Single')
	profile_pic = models.ImageField(upload_to = 'profile_images', blank=True,default=default_profile)
	cover_pic = models.ImageField(upload_to = 'cover_images', blank=True,default=default_cover)



	def __str__(self):
		return '%s %s' %(self.user.username, self.bio)
# 


	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()