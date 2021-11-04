from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default ='default.png', upload_to='profile_pics')
    height = models.CharField(max_length = 10)
    #Date of Birth
    dob = models.DateTimeField(default=timezone.now)
    #ToDO (Kenneth)  Tempoary PlaceHolder for the sports colum
    sports = models.TextField(default = 'No Sports Played')

    def __str__(self):
        return f'{self.user.username} Profile'
