from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('forgot-password/', auth_views.PasswordResetView.as_view(
         template_name='forgot_password.html',
         email_template_name='password_reset_email.html',
         subject_template_name='password_reset_subject.txt',
         success_url='/password-reset-done/'
    ), name='password_reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
         template_name='password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
         template_name='password_reset_confirm.html',
         success_url='/password-reset-complete/'
    ), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
         template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
]