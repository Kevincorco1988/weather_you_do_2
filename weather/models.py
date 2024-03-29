from django.db import models
from users.models import Profile
from decimal import Decimal


class Favourite(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=254, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensures a user can only add a favorite city once
        unique_together = ('owner', 'city_name')

    def save(self, *args, **kwargs):
        self.city_name = self.city_name.lower()
        return super(Favourite, self).save(*args, **kwargs)

    def __str__(self):
        # String representation showing the user and the favorite city_name
        return f"{self.owner.username}'s favorite {self.city_name}"



class HourlyForecast(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=254, null=False, blank=False)
    fcast_date = models.DateField()
    avg = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    hours_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        # Ensures a user can only add a favorite city once
        unique_together = ('owner', 'city_name', 'fcast_date')

    def save(self, *args, **kwargs):
        self.city_name = self.city_name.lower()
        return super(HourlyForecast, self).save(*args, **kwargs)

    def __str__(self):
        # String representation showing the user and the favorite city_name
        return f"{self.owner.username} - {self.city_name} - {self.fcast_date.strftime('%m/%d/%Y')}"
