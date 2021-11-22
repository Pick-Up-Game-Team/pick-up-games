from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship

#This is used so that once a user is created, we also create a profile for it.
@receiver(post_save, sender = User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender = User)
def save_profile(sender,instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, created, instance, **kwargs):
    # instance: an instance of our Relationship model
    # sender_ and receiver_ are foreign keys for the Realtionship model I believe

    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()


@receiver(post_save, sender=Relationship)
def post_remove_from_friends(sender, created, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'delete':
        sender_.friends.remove(receiver_.user)
        receiver_.friends.remove(sender_.user)
        sender_.save()
        receiver_.save()
        instance.delete()

@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()






