from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # creating our own save method/ overwriting the save method
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        # make instance of image and pass the path to it
        img = Image.open(self.image.path)

        # resizing the image.
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


@receiver(post_save, sender=User)
def create_user_info_on_user_creation(instance, *args, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=instance)
