from django.urls import path, reverse_lazy, re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [ 
    #path('', PasswordResetView.as_view(), {'post_reset_redirect': reverse_lazy('users:password_reset_done')}, name='password_reset'),
    path('',auth_views.PasswordResetView.as_view(template_name='password_reset.html',success_url=reverse_lazy('users:password_reset_done'),email_template_name='password_reset_email.html'),name='password_reset'),
    path('done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('<str:uidb64>/<str:token>',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',success_url=reverse_lazy('users:password_reset_complete')),name='password_reset_confirm'),
    path('complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),  
]
