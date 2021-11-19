from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, Relationship

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
    # Allows us to use our the profile object in our template
    myprofile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        # updates username and password
        u_form = UserUpdateForm(request.POST, instance = request.user)

        # updates profile picture
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance = request.user.profile)

        if u_form.is_valid() and p_form.is_valid: # save if valid
            u_form.save()
            p_form.save()

            messages.success(request,f'Account updated!')
            return redirect('profile')
    else:
        # updates username and password
        u_form = UserUpdateForm(instance = request.user)
        # updates profile picture
        p_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': myprofile
    }

    return render(request, 'users/profile.html', context)

def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)

    context = {'qs': qs}
    return render(request, 'users/my_invites.html', context)
