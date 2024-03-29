from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile
from .models import Favourite, HourlyForecast
from datetime import datetime

class TestFavourite_HourlyForecastModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                username='testuser', password='12345', email='ex@example.com')
        self.user_profile = Profile.objects.get(user=self.user,
            username=self.user.username,
            email=self.user.email,
            name=self.user.username)
        self.user_favourite = Favourite.objects.create(owner=self.user_profile, city_name='ATHENs')
        dt = datetime.today().date()
        self.user_hourlyforecast = HourlyForecast.objects.create(owner=self.user_profile, city_name='athens', fcast_date=dt, avg=32.3, hours_count=24)
    
    def test_favourite_model_str(self):
        self.assertEqual(self.user_favourite.__str__(), f"{self.user_favourite.owner.username}'s favorite {self.user_favourite.city_name}")
        
    
    def test_favourite_model_city_name(self):
        self.assertEqual(self.user_favourite.city_name, 'athens')

    def test_hourlyforecast_model_str(self):
        self.assertEqual(self.user_hourlyforecast.__str__(), f"{self.user_hourlyforecast.owner.username} - {self.user_hourlyforecast.city_name} - {self.user_hourlyforecast.fcast_date.strftime('%m/%d/%Y')}")
        

    def test_hourlyforecast_model_avg_date(self):
        self.assertEqual(self.user_hourlyforecast.avg, 32.3)
        self.assertEqual(self.user_hourlyforecast.fcast_date, datetime.today().date())
