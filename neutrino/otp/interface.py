from random import randint
from neutrino.otp.service.core import EmailFactroyMethod , SmsFactroyMethod
from neutrino.otp.service.SmsProvider import KavenegarProvider , TestProvider
from config.env import env
from .models import TESTMODELOTP
from django.utils import timezone
import os 
import binascii

token =  lambda  : binascii.hexlify(os.urandom(20)).decode()

_rand_numberOTP = lambda length : ''.join([str(randint(0,9)) for i in range(length)])
from rest_framework.authtoken.models import Token

def send_otp_sms(phone_number ,**kwargs)->str:
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
    token_str = token()
    # provider_object = KavenegarProvider(
    #         apikey=env('KAVENEGAR_TOKEN') 
    #     )
    provider_object = TestProvider()
    from neutrino.otp.models import Mailsystem , SmsSystem
    import logging
    service = SmsFactroyMethod(
            provider= provider_object , 
            Log_model=SmsSystem ,
            Logger_factory=logging.getLogger('SmsOtp') , 
            sender = '09932667257' , # sender from Parsa
            receiver=phone_number ,
            subject='This is otp number' , 
            message=token_ # OTP code 
        )
        
    service.send_message() 
        # adding token to the redis 
        # phone token aeempet time code 
        
    TESTMODELOTP.objects.create(
            token = token_str, 
            phone = phone_number , 
            attempet = total_attempet , # Settings defualt attrempet
            code = token_
        
        ) # save  
    return token_str 



def main():
    print(
        send_otp_sms('09932667257') 
    )

if __name__ == '__main__':main()
# sms OTP is up 

class OtpError(BaseException):
    def __init__(self, *args):
        if args:
            self.code = args[0]
        super().__init__(*args)
    ERROR_CODE = ''
    
    def __str__(self):
        return f'{self.__class__.__name__}({self.code if self.code else self.ERROR_CODE})'

class ExpiredOtpToken(OtpError):
    ERROR_CODE = 'Expired Token this is verifiy'

class CodeOtpnoteMatch(OtpError):
    ERROR_CODE = 'otp code from  oken is not match'

class TomanyAttempetOtp(OtpError):
    ERROR_CODE = 'to many atempet from token'


def verify_otp(token , code)-> TESTMODELOTP | None:
    # check_token_is_exist
    '''
    TODO we shoud have altartion in this alogritm because 
    we must now how impement about expid time 
    '''
    # try :
    token_model = TESTMODELOTP.objects.get(
            token = token
        )
    print('that token is here', token_model)
    # except Exception as e :
    #     raise OtpError(f'invalid token \n \' {e}')
    

    save =  lambda : token_model.save()
        
    if token_model.is_verified :
        raise  ExpiredOtpToken('this token was verifid'  ,token_model.token)


    elif token_model.attempet == 0 :

        token_model.attempet == 3 
        save()
        raise TomanyAttempetOtp('To many attempetd')

    else : 
        if token_model.code == code:
            # check the best 
            token_model.is_verified = True 
            save()
            return token 
        else:
            token_model.attempet -= 1 
            save()
            raise CodeOtpnoteMatch('this code is not valid')
            