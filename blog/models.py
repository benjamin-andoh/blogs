from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # reverse will return the full url to the rout as a string
    # so we will return the string and let the view handle
    # the rest for us.
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
