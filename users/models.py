from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default ='default.jpg', upload_to='profile_pics')
    height = models.CharField(max_length = 10)
    #Date of Birth
    dob = models.DateTimeField()
    #ToDO (Kenneth)  Tempoary PlaceHolder for the sports colum
    sports = models.TextField(default = 'No Sports Played')

    def __str__(self):
        return f'{self.user.username} Profile'


