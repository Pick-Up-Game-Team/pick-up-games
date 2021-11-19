from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Report
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserReportForm

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
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def report_user(request):
    """
    View that displays form to report a user with a message for admins to review
    """
    # Get the username of the reported user from query string
    author = request.user.username
    target_user = request.GET.get('user', None)

    # If no username is given, redirect to home page
    if target_user == None:
        return redirect('home-page')

    # If there is no user that matches the passed username,
    # output error and redirect to home page
    if not User.objects.filter(username=target_user).exists():
        messages.error(request,f'Report error: User not found.')
        return redirect('home-page')

    # Handle submissions
    if request.method == 'POST':
        report = Report(author=User.objects.get(username=author), 
                        reported_user=User.objects.get(username=target_user))
        
        form = UserReportForm(request.POST, instance=report)

        # Validate form data and save, confirmation message and redirect
        if form.is_valid():
            form.save()
            messages.success(request,f'Thank you for submitting a user report.')
            return redirect('home-page')
    # GET request, display form page
    else:
        form = UserReportForm()

    context = {
        'title': f'Report User',
        'form': form,
        'target_user': target_user
    }

    return render(request, 'users/report.html', context)