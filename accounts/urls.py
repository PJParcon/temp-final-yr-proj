from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('medications/', views.medications_placeholder, name='medications'),
    path('schedule/', views.schedule_placeholder, name='schedule'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_update, name='profile_update'),
    path('profile/delete/', views.account_delete, name='account_delete'),
    path('password/change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url=reverse_lazy('accounts:password_change_done'),
    ), name='password_change'),
    path('password/changed/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html',
    ), name='password_change_done'),
    path('register/', views.register, name='register'),
    path('registration-complete/', views.registration_complete, name='registration_complete'),
]
