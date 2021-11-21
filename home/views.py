from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home/home-page.html')

def search(request):
    if request.method == "POST":
        results = request.POST['results']
        queries = User.objects.filter(username__contains=results)
        return render(request, 'home/search.html', {'results':results, 'queries':queries})
    else:
        return render(request, 'home/search.html')
