from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm


# for change password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User








@login_required
def index(request):
    return redirect('chats')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})



# change password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('index')
        else:
            messages.error(request, _('Please correct the error below.'))
            return redirect('change_password')
    else:
        form = PasswordChangeForm(user =request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
})