from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Profile
from .models import Favourite


class TestWeatherViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                username='testuser', password='12345')
        self.user_profile = Profile.objects.get(user=self.user)

    def test_index_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('weather:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/index.html')

    def test_current_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/current/', {'city_name': 'athens'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/current.html')
        self.assertIn('current_weather', response.context)

    def test_hourly_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/hourly/', {'city_name': 'athens'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/hourly.html')
        self.assertIn('grouped_forecast', response.context)
        self.assertIn('form', response.context)
        self.assertNotEqual(len(response.client.session['hfcast']), 0)
        response = self.client.post(
                    reverse('weather:hourly'),
                    data={'city_name': 'athens'}
        )
        self.assertRedirects(response, reverse('weather:hourlyFcastCity', args=['athens']))

    def test_add_favourites_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/add_to_favorites/athens/')
        f = Favourite.objects.count()
        self.assertEqual(f, 1)

    def test_remove_favourites_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/remove_from_favorites/athens/')
        f = Favourite.objects.count()
        self.assertEqual(f, 0)

    def test_favourites_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/favourites/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/favourites.html')
        self.assertIn('favorite_cities', response.context)

    def test_hourlyfcast_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/hourly/athens/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/hourlyFcast.html')
        self.assertIn('fcast', response.context)
