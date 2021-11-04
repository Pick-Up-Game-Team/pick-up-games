from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm

def register(request):
    #This one will create the actual user creation form
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        #Valid user data, print message and redirect to homepage
        if form.is_valid():
            form.save()#Saves the actual user form and does hashing stuff
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {
        'title': 'Registration',
        'form': form,
    }

    return render(request, 'users/registration-page.html', context)

    @login_required
    def profile(request):
        u_form = UserUpdateForm # updates usename and password
        p_form = ProfileUpdateForm # updates profile picture

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

        return render(request, 'users/profile-page.html', context)
