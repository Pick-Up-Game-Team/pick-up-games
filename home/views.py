from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Home page currently in progress. This is here temporarily :)")