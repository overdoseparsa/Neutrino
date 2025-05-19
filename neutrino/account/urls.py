from django.urls import path
from neutrino.account.ViewService.api import ProfileViewApi
from neutrino.account.ViewService.api import CreateAccountApiView
app_name = 'account'

urlpatterns = [
    path('<int:id>/' , ProfileViewApi.as_view() , name='account_profile') , 
    path('' , CreateAccountApiView.as_view() , name='create_accou' ) ,  
]
