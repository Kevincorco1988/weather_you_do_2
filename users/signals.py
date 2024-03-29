from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile

# Signal receiver function to create a profile when a new user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.username
        )

# Signal receiver function to update user information when profile is edited
@receiver(post_save, sender=Profile)
def edit_profile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created is False:
        user.name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

# Signal receiver function to delete user when profile is deleted
@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except Exception:
        pass

