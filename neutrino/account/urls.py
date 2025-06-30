from django.urls import path
from neutrino.account.SignService.api import ROUAT_SIGN_API
from neutrino.account.LogginService.api import LOGGIN_URLS_PATH , LOGGIN_USERNAME_API
app_name = 'account'

urlpatterns = [
    ROUAT_SIGN_API  , 
    LOGGIN_URLS_PATH , 
    LOGGIN_USERNAME_API
]
