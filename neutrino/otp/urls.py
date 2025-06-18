from django.urls import path , include 
from .views import SmsOtpSendApi


urlpatterns = [
    path('send_otp/' , SmsOtpSendApi.as_view() , name='send_otp')    
]  

