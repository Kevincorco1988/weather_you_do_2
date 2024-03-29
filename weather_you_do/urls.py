from django.contrib import admin
from django.urls import path, include
from .views import handler403, handler404, handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls')),
    path('users/', include ('users.urls')),
]

handler403 = handler403
handler404 = handler404
handler500 = handler500
