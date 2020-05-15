from django.urls import path
from .views import LoginView, RegisterView, ProfileView, ProfileSettings, ChangePersonalDetails
from django.contrib.auth.views import LogoutView

app_name = 'authentication'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_url'),
    path('register/', RegisterView.as_view(), name='register_url'),
    path('', ProfileView.as_view(), name='profile_url'),
    path('settings/', ProfileSettings.as_view(), name='profile_settings'),
    path('settings/personal_details/', ChangePersonalDetails.as_view(), name='personal_details_settings'),
    path('settings/logout', LogoutView.as_view(), name='logout_url'),
]