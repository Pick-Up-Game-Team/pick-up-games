from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from PIL import Image


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    height = models.CharField(default='0', max_length=10)
    # Date of Birth
    dob = models.DateTimeField(default=timezone.now)
    # ToDO (Kenneth)  Tempoary PlaceHolder for the sports colum
    sports = models.TextField(default='No Sports Played')

    # friends stuff
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    # bio = models.TextField()

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # save image for editing
        super().save(*args, **kwargs)
        profileIMG = Image.open(self.image.path)

        # resizing image
        if profileIMG.height > 300 or profileIMG.width > 300:
            output_size = (300, 300)
            profileIMG.thumbnail(output_size)
            profileIMG.save(self.image.path)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'),
    ('delete', 'delete'),
)


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # String representation of our Relationship model
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
