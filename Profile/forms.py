from django import forms
from .models import Profile




class ProfileForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ('bio', 'location', 'birth_date', 'maritial_status', 'profile_pic', 'cover_pic')
	