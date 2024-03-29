from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Profile


class TestProfileViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                username='testuser', password='12345')
        self.user_profile = Profile.objects.get(user=self.user)

    def test_login_and_get_profile_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('users:profile', args=[self.user_profile.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertIn('profile', response.context)

    def test_edit_account(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
                    reverse('users:edit_account'),
                    data={'name': 'test', 'username': 'test', 'image': SimpleUploadedFile(
        name='background.jpg', content=open('static/images/background.jpg', 'rb').read(), content_type='image/jpeg'), 'email':'at@fake.com'})
        self.assertRedirects(response, reverse('users:profile', args=[self.user_profile.pk]))

    def test_delete_account(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
                    reverse('users:delete_account'), args=[self.user_profile.pk]
        )
        self.assertEqual(response.status_code, 302)
        p = Profile.objects.count()
        self.assertEqual(p, 0)