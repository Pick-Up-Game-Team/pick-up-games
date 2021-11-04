from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default ='default.png', upload_to='profile_pics')
    height = models.CharField(default='0', max_length=10)
    #Date of Birth
    dob = models.DateTimeField(default=timezone.now)
    #ToDO (Kenneth)  Tempoary PlaceHolder for the sports colum
    sports = models.TextField(default = 'No Sports Played')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        # save image for editing
        super().save()
        profileIMG = Image.open(self.image.path)

        # resizing image
        if profileIMG.height >  300 or profileIMG.width > 300:
            output_size = (300, 300)
            profileIMG.thumbnail(output_size)
            profileIMG.save(self.image.path)
