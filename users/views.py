from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, Relationship
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.models import User
from .models import Report
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserReportForm


def register(request):
    # This one will create the actual user creation form
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        # Valid user data, print message and redirect to homepage
        if form.is_valid():
            form.save()  # Saves the actual user form and does hashing stuff
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
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
        u_form = UserUpdateForm(request.POST, instance=request.user)

        # updates profile picture
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid:  # save if valid
            u_form.save()
            p_form.save()

            messages.success(request, f'Account updated!')
            return redirect('profile')
    else:
        # updates username and password
        u_form = UserUpdateForm(instance=request.user)
        # updates profile picture
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': myprofile
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
        messages.error(request, f'Report error: User not found.')
        return redirect('home-page')

    # Handle submissions
    if request.method == 'POST':
        report = Report(author=User.objects.get(username=author),
                        reported_user=User.objects.get(username=target_user))

        form = UserReportForm(request.POST, instance=report)

        # Validate form data and save, confirmation message and redirect
        if form.is_valid():
            form.save()
            messages.success(request, f'Thank you for submitting a user report.')
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


def invites_received_view(request):
    aprofile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(aprofile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'qs': results,
        'is_empty': is_empty,
    }
    return render(request, 'users/my_invites.html', context)


def accept_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('my-invites-view')


def reject_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('my-invites-view')


def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}
    return render(request, 'users/to_invite_list.html', context)


def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs': qs}
    return render(request, 'users/profile_list.html', context)


class ProfileListView(ListView):
    model = Profile
    template_name = 'users/profile_list.html'

    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)

        # Checking the relationships of our profile
        # Querying by receiver (then sender) equal to profile

        # Relationships where we invited other people to be friends
        rel_r = Relationship.objects.filter(sender=profile)
        # Relationships where others invited us
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False

        # We're the only profile
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context


def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        # create a relationship
        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        # Keeps us on same page
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile:profile')


def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        # Don't know who the remover is -> more complicated lookup

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver))  # Case 1: We invited someone, they accepted, now we remove them
            | (Q(sender=receiver) & Q(receiver=sender))  # Case 2: Someone invited us, we accepted, now we remove them
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile:profile')
