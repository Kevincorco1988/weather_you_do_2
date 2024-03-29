from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class TestProfileModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                username='testuser', password='12345', email='ex@example.com')
        self.user_profile = Profile.objects.get(user=self.user,
            username=self.user.username,
            email=self.user.email,
            name=self.user.username)

    def test_profile_model_str(self):
        self.assertEqual(self.user_profile.__str__(), f'{self.user_profile.username} Profile')

    def test_profile_model_email(self):
        self.assertEqual(self.user_profile.email, 'ex@example.com')