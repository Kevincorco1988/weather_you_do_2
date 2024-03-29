from django.test import TestCase
from .forms import ProfileForm, UserRegisterForm
from django.core.files.uploadedfile import SimpleUploadedFile


class TestProfileForm(TestCase):

    def test_fields_are_explicit_in_forms_metaclass(self):
        form = ProfileForm()
        self.assertEqual(form.Meta.fields, ['name', 'username', 'email', 'image'])


    def test_profile_form_valid(self):
        form = UserRegisterForm({'username': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors.keys())
        self.assertEqual(form.errors['username'][0], 'This field is required.')
        form = ProfileForm({'name': 'test', 'username': 'test', 'image': SimpleUploadedFile(
        name='background.jpg', content=open('static/images/background.jpg', 'rb').read(), content_type='image/jpeg'), 'email':'at@fake.com'})
        self.assertTrue(form.is_valid())