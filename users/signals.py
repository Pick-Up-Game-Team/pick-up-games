from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

#This is used so that once a user is created, we also create a profile for it.
@receiver(post_save, sender = User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender = User)
def save_profile(sender,instance, **kwargs):
    instance.profile.save()