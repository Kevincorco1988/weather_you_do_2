from django.urls import path, include
from . import views
from django.conf import settings  
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users import url_reset

# Set the application namespace
app_name = 'users'

# Define URL patterns
urlpatterns = [
    # User registration
    path('register/', views.register, name='register'),
    
    # User login
    path('login/', views.login, name='login'),
    
    # User logout
    path('logout/', views.logout_view, name='logout'),
    
    # User profile
    path('profile/<int:pk>/', views.profile, name='profile'),
    
    # Edit user account
    path('edit_account/', views.edit_account, name='edit_account'),
    
    # Delete user account
    path('delete_account/', views.delete_account, name='delete_account'),
    
    # Password reset
    path('password-reset/', include('users.url_reset')),
]   



