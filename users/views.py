from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    #This one will create the actual user creation form
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        #Valid user data, print message and redirect to homepage
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('home-page')
    else:
        form = UserCreationForm()
    return render(request, 'users/registration-page.html', {'form': form})