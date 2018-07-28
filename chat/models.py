from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class Online_User(models.Model):
    status_choices= ((0,'Offline'),(1,'Online'),)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    status=models.CharField(max_length=3,choices=status_choices,default=0)
    session_time= models.DateTimeField(auto_now_add=True)

def create_status(sender,**kwargs):
    if kwargs['created']:
        Onl=Online_User.objects.create(user=kwargs['instance'])
class Record(models.Model):
	IMAGE_CHOICES = (
        (0, 'NotAdded'),
        (1, 'Added'),
    )
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	image_added=models.CharField(max_length=3,choices=IMAGE_CHOICES,default=0)

def create_image(sender,**kwargs):
	if kwargs['created']:
		Ima=Record.objects.create(user=kwargs['instance'])

post_save.connect(create_image,sender=User)
post_save.connect(create_status,sender=User)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    # senderview=models.CharField(max_length=20,default="View")
    # receiverview=models.CharField(max_length=20,default="View")

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)

# class Online(models.Model):
#     users = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')           
#     is_online = models.BooleanField(default=False)


