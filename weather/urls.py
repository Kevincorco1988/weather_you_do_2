from django.urls import path
from .import views

app_name = 'weather'

urlpatterns = [
    path('', views.index, name='index'),
    path('current/', views.current, name='current'),
    path('hourly/', views.hourly, name='hourly'),
    path('favourites/', views.favourites, name='favourites'),
    path('add_to_favorites/<str:city_name>/', views.add_to_favorites, name='add_to_favorites'), # noqa
    path('remove_from_favorites/<str:city_name>/', views.remove_from_favorites, name='remove_from_favorites'),
]