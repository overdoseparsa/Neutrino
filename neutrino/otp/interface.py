from random import randint
from neutrino.otp.service.core import EmailFactroyMethod , SmsFactroyMethod
from neutrino.otp.service.SmsProvider import KavenegarProvider , TestProvider
from config.env import env
from .models import TESTMODELOTP
from django.utils import timezone
import os 
import binascii

token =  binascii.hexlify(os.urandom(20)).decode()

_rand_numberOTP = lambda length : ''.join([str(randint(0,9)) for i in range(length)])
from rest_framework.authtoken.models import Token

def send_otp_sms(phone_number)->str:
    total_attempet = 3
    """
        # TODO change to the redis     
        # TODO more Scable code just for test this i
        Maybe we want ti chech that service 
        we want to send message Otp 
        we have to use good sturcture and more adaptable and 
        readbale 

        
        class RedisOtpCilent():
            def __init__(self):
                # logicconnection 
            def check_attempet(self):
                # logic 1 
            def save_the_token(self):
                # logic 1 

        class DatabaseCilent():
            def __init__(self):
                # logicconnection 
            def check_attempet(self):
                # logic 2 
                # is  OtpModel.object.get('token') is 
                expried 
                # changee the logic 
            def save_the_token(self):
                # logic 2 

        class AnotherFactroy ... 
        class SendOtpSms:
            service = RedisOtpCileent
            def check_validation():
                service.check_validation_from_redis()
    or maybe we want to change the altration from service 
    # that code should have a desin or a structre it is adaptable and i dont need 
    to change from core off project 
    SO TODO we have alration from this code 
    and it is import how to add the email base
    """

    token_ = _rand_numberOTP(6)
    # provider_object = KavenegarProvider(
    #         apikey=env('KAVENEGAR_TOKEN') 
    #     )
    provider_object = TestProvider()
    service = SmsFactroyMethod(
            provider= provider_object , 
            sender = '09932667257' , # sender from Parsa
            receiver=phone_number ,
            subject='This is otp number' , 
            message=token_ # OTP code 
        )
        
    service.send_message() 
        # adding token to the redis 
        # phone token aeempet time code 
        
    TESTMODELOTP.objects.create(
            token = token_ , 
            phone = phone_number , 
            attempet = total_attempet , # Settings defualt attrempet
            time_expired = timezone.now() 


        ) # save 
    return token_ 





