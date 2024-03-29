from django.test import TestCase
from .forms import HourlyFcastForm


class TestHourlyFcastForm(TestCase):

    # test that message value needs to be provided
    def test_city_name_is_required(self):
        form = HourlyFcastForm({'city_name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('city_name', form.errors.keys())
        self.assertEqual(form.errors['city_name'][0], 'This field is required')
