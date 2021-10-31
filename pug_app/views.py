# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse


def index(request):
    return render(request, 'pug_app/index.html')
