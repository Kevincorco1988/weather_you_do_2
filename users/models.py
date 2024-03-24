from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=80, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return f'{self.user.username} Profile'
