from django.contrib import admin

# Register your models here.
from .models import City, Court

admin.site.register(City)
admin.site.register(Court)