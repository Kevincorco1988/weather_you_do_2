from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Model for user profiles
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User model
    name = models.CharField(max_length=200, blank=True, null=True)  # Name of the user
    username = models.CharField(max_length=80, blank=True, null=True)  # Username of the user
    email = models.EmailField(max_length=500, blank=True, null=True)  # Email of the user
    image = CloudinaryField('image', default='placeholder')  # Profile image stored on Cloudinary

    # String representation of the Profile model
    def __str__(self):
        return f'{self.user.username} Profile'


