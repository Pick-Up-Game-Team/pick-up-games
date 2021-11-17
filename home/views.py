from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home/home-page.html')

def search(request):
    if request.method == "POST":
        results = request.POST['results']
        return render(request, 'home/search.html', {'results':results})
    else:
        return render(request, 'home/search.html')
