from django.urls import path  # Importing necessary modules
from . import views  # Importing views from the same directory

app_name = 'weather'  # Declaring the app namespace

urlpatterns = [
    path('', views.index, name='index'),  # URL pattern for the index page
    path('current/', views.current, name='current'),  # URL pattern for the current weather page
    path('hourly/', views.hourly, name='hourly'),  # URL pattern for the hourly forecast page
    path('favourites/', views.favourites, name='favourites'),  # URL pattern for the favourites page
    path('add_to_favorites/<str:city_name>/', views.add_to_favorites, name='add_to_favorites'),  # URL pattern for adding a city to favourites
    path('remove_from_favorites/<str:city_name>/', views.remove_from_favorites, name='remove_from_favorites'),  # URL pattern for removing a city from favourites
    path('hourly/<str:city_name>/', views.hourlyFcastCity, name="hourlyFcastCity")  # URL pattern for the hourly forecast of a specific city
]
