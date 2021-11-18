from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm

def register(request):
    # This one will create the actual user creation form
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        # Valid user data, print message and redirect to homepage
        if form.is_valid():
            form.save() # Saves the actual user form and does hashing stuff
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'title': 'Registration',
        'form': form,
    }

    return render(request, 'users/registration.html', context)

@login_required
def profile(request):
    return render(request, 'users/public-page.html')

def manage(request):
    if request.method == 'POST':
        # updates username and password
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():  # save if valid
            u_form.save()

            messages.success(request, f'Account updated!')
            return redirect('profile')
    else:
        # updates username and password
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }

    return render(request, 'users/account-management.html', context)


def change(request):
    if request.method == 'POST':

        # updates profile picture and profile fields
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if p_form.is_valid:  # save if valid
            p_form.save()

            messages.success(request, f'Account updated!')
            return redirect('profile')
    else:

        # updates profile picture
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)