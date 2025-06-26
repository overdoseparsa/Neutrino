from django.urls import path
from neutrino.account.SignService.api import ROUAT_SIGN_API
app_name = 'account'

urlpatterns = [
    ROUAT_SIGN_API
]
