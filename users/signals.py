from django.db.models.signals import post_save
# the sender
from django.contrib.auth.models import User
# the receiver
from django.dispatch import receiver
from .models import Profile


# we want a user profile to be created for each new user
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=instance)


# the user is the instance
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()