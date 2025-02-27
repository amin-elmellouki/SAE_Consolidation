from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('forgot_password/', auth_views.PasswordResetView.as_view(
         template_name='forgot_password.html',
         email_template_name='password_reset_email.html',
         subject_template_name='password_reset_subject.txt',
         success_url='/password_reset_done/'
    ), name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
         template_name='password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
         template_name='password_reset_confirm.html',
         success_url='/password_reset_complete/'
    ), name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
         template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
]
