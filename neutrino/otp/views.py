from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.exceptions import bad_request

from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from abc import ABC, abstractmethod
from neutrino.account.validator import PhoneValidator 
from django.core.validators import MaxLengthValidator , integer_validator
import logging 


class BaseOtpApi(APIView):
    # save in database 
    # logs 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger_api = self.get_logger()

    def dispatch(self, request, *args, **kwargs):
        self.logger_api.info(f'the request from  sms_api_ and Method is {request.method}')
        return super().dispatch(request, *args, **kwargs)
    _sms_api_logger = logging.getLogger('SmsSendApilogs')
    InputSerializer = ... 
    OutputSerializer = ... 

    @abstractmethod
    def otp_process(self , data ,  **kwargs)->dict:
        
        'send the otp requests and return Token'
        # send Otp 
        # save in redis 
        # check_in_valiation 
        # return str_token 
    def get_logger(self)->logging.Logger:
        assert isinstance(self._sms_api_logger , logging.Logger) , "the sms api logger mus be instance from logger" 
        return  self._sms_api_logger    
      
    
    @property
    def get_input_serializer(self)->serializers.Serializer:
        return self.InputSerializer
    

    @property
    def get_output_serialzer(self)->serializers.Serializer:
        return self.OutputSerializer
    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self , request , **kwargs)->Response:
        self.logger_api.info(f'the pyload from Sms requested is {self.request.POST} ' , )
        
        input_serailizer = self.get_input_serializer(data = request.POST) # property 
        try:
            input_serailizer.is_valid(raise_exception=True)
            response = self.otp_process(input_serailizer.data , **kwargs)
        except BaseException as e:
            print('InterNullERROR ' , e)
            return bad_request(request , e)

        outputserializer = self.get_output_serialzer(data = response)
        outputserializer.is_valid()

        return Response(outputserializer.data , status=HTTP_201_CREATED)
        
from .interface import (
    send_otp_sms ,   verify_otp  
)

# urls 

class SmsOtpSendApi(BaseOtpApi):
    
    class OTPInSerailizer(serializers.Serializer):
        phone = serializers.CharField(
            validators = [PhoneValidator('Is Not Valid Phone','no_valid_code')]
        )
   
    InputSerializer  = OTPInSerailizer
    
    class OTPOutSerailizer(serializers.Serializer):
        token = serializers.CharField()
        rate_limite = serializers.IntegerField()
    
    OutputSerializer = OTPOutSerailizer
    def otp_process(self, data, **kwargs):
        token  = send_otp_sms(phone_number=data['phone'])
        return {
            'token':token , 
        }
    def post(self, request, **kwargs):
        return super().post(request, **kwargs)
    
# TODO 
# add the Email app 


class PhoneVerifyApi(BaseOtpApi):
    class InputVerifySerailizer(serializers.Serializer):
        token = serializers.CharField()
        otp_code = serializers.CharField(
            validators = [
                MaxLengthValidator(10) , 
                integer_validator
            ]
        )

    class OutputVerifySerializer(serializers.Serializer):
        token = serializers.CharField()

    InputSerializer  = InputVerifySerailizer
    OutputSerializer = OutputVerifySerializer 

    def post(self, request, **kwargs):
        return super().post(request, **kwargs)    

    @abstractmethod
    def otp_process(self, data, **kwargs)-> str|None:
        print('Pyload from Otp:...process' , data)
        return verify_otp(
            token=data['token'] , 
            code = data['otp_code'] , 
        )


    
    