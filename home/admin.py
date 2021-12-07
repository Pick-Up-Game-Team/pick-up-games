from django.contrib import admin

# Register your models here.
from .models import City, Venue

admin.site.register(City)
admin.site.register(Venue)