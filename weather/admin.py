from django.contrib import admin
from .models import Favourite, HourlyForecast


admin.site.register(Favourite)
admin.site.register(HourlyForecast)