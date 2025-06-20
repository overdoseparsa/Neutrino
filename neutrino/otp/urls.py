from django.urls import path , include 
from .views import SmsOtpSendApi , PhoneVerifyApi


urlpatterns = [
    path(
        'sms/' , include(
            ([
            path('send/' , SmsOtpSendApi.as_view() , name='send_sms')    , 
            path('verify/' , PhoneVerifyApi.as_view() , name='verify_sms') , 
            ])
        )
    )

]



