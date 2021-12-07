from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from datetime import date
from PIL import Image
from django.db.models import Q


# Create your models here.

class ProfileManager(models.Manager):

    # All profiles we can invite; not ourselves or ones we're already friends with
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)

        # Query Set of all relationships we're not involved in
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        # Creating our list of stuff we don't want displayed
        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)

        # All the profiles we can friend request
        available = [profile for profile in profiles if profile not in accepted]
        return available



    # Returns all profiles except yours
    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default ='default.png', upload_to='profile_pics')
    # Height in inches
    height = models.IntegerField(default=60)
    #Date of Birth
    dob = models.DateField(default=timezone.now)
    #ToDO (Kenneth)  Tempoary PlaceHolder for the sports colum
    sports = models.TextField(default = 'No Sports Played')

    # friends stuff
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    objects = ProfileManager()

    #Used to check if the user is online
    is_online = models.BooleanField(default = False)


    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # save image for editing
        super(Profile,self).save(*args, **kwargs)
        profileIMG = Image.open(self.image.path)

        # resizing image
        if profileIMG.height > 300 or profileIMG.width > 300:
            output_size = (300, 300)
            profileIMG.thumbnail(output_size)
            profileIMG.save(self.image.path)

    def calculate_age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    def calculate_height(self):
        feet = int(self.height/12)
        inches = self.height % 12

        return f"{feet}'{inches}\""

class Report(models.Model):
    # Description of report
    message = models.CharField(max_length=2000)

    # Many-to-one relationship; a User may be the author or reported_user
    # of multiple Reports. When a related user is deleted, the Report will be deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

    # Report objects will be displayed as "Report - <reported_user>"
    def __str__(self):
        return f'Report - {self.reported_user.username}'


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'),
    ('delete', 'delete'),
)


class RelationshipManager(models.Manager):

    def invitations_received(self, receiver):
        # qs - Query Set
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # Extending our existing manager
    objects = RelationshipManager()

    # String representation of our Relationship model
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
