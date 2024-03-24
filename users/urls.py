from django.urls import path
from .import views
from django.conf import settings  
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('delete_account/', views.delete_account, name='delete_account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)