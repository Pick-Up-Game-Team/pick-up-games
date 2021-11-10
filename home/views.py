from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'home/home-page.html')


def support(request):
    return render(request, 'home/support.html')


def about(request):
    return render(request, 'home/about.html')
