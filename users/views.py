from django.shortcuts import render
from django.contrib.auth import UserCreationForm
def register(request):
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

