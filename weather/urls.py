from django.urls import path
from .import views

app_name = 'weather'

urlpatterns = [
    path('', views.index, name='index'),
    path('current/', views.current, name='current'),
    path('hourly/', views.hourly, name='hourly'),
]