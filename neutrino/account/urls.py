from django.urls import path
from neutrino.account.ViewService.api import ProfileViewApi
app_name = 'account'
urlpatterns = [
    path('<int:id>/' , ProfileViewApi.as_view() , name='account_profile')
]
