from django.db import models  # Importing necessary modules
from users.models import Profile  # Importing the Profile model from the users app
from decimal import Decimal  # Importing Decimal for handling decimal numbers

class Favourite(models.Model):  # Defines a model for storing favorite cities
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Relationship with the user's profile
    city_name = models.CharField(max_length=254, null=False, blank=False)  # Name of the favorite city
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for last update

    class Meta:
        # Ensures that a user can only add a favorite city once
        unique_together = ('owner', 'city_name')

    def save(self, *args, **kwargs):  # Overrides save method to ensure uniformity in city names
        self.city_name = self.city_name.lower()  # Converts city name to lowercase
        return super(Favourite, self).save(*args, **kwargs)  # Calls the parent class's save method

    def __str__(self):  # Defines a string representation for the model
        # String representation showing the user and the favorite city_name
        return f"{self.owner.username}'s favorite {self.city_name}"


class HourlyForecast(models.Model):  # Defines a model for storing hourly forecasts
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Relationship with the user's profile
    city_name = models.CharField(max_length=254, null=False, blank=False)  # Name of the city
    fcast_date = models.DateField()  # Forecast date
    avg = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))  # Average temperature
    hours_count = models.PositiveSmallIntegerField(default=0)  # Number of forecast hours

    class Meta:
        # Ensures that a user can only add a forecast for a city on a specific date once
        unique_together = ('owner', 'city_name', 'fcast_date')

    def save(self, *args, **kwargs):  # Overrides save method to ensure uniformity in city names
        self.city_name = self.city_name.lower()  # Converts city name to lowercase
        return super(HourlyForecast, self).save(*args, **kwargs)  # Calls the parent class's save method

    def __str__(self):  # Define a string representation for the model
        # String representation showing the user, city_name, and forecast date
        return f"{self.owner.username} - {self.city_name} - {self.fcast_date.strftime('%m/%d/%Y')}"

