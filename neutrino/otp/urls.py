from django.urls import path , include 
from .views import SmsOtpSendApi


urlpatterns = [
    path('sms/' , SmsOtpSendApi.as_view() , name='send_otp')    
]  
