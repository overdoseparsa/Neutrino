from django.urls import path
from neutrino.account.ViewService.api import ProfileViewApi
from neutrino.account.auth_sign.api import SignAccountApi
app_name = 'account'

urlpatterns = [
    path('sign/', SignAccountApi.as_view(), name='account_signup') ,   
]
