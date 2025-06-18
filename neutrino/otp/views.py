from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.exceptions import bad_request

from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from abc import ABC, abstractmethod
from neutrino.account.validator import PhoneValidator




class BaseOtpSendApi(APIView):
    # save in database 
    # logs 
    InputSerializer = ... 
    class OTPOutSerailizer(serializers.Serializer):
        token = serializers.CharField()    
    @abstractmethod
    def otp_process(self , data ,  **kwargs)->dict:
        'send the otp requests and return Token'
        # send Otp 
        # save in redis 
        # check_in_valiation 
        # return str_token 
    @property
    def get_input_serializer(self)->serializers.Serializer:
        return self.InputSerializer
    @extend_schema(request=InputSerializer, responses=OTPOutSerailizer)
    def post(self , request , **kwargs)->Response:
        input_serailizer = self.get_input_serializer(data = request.POST) # property 
        try:
            input_serailizer.is_valid(raise_exception=True)
            response = self.otp_process(self ,input_serailizer.data , **kwargs)
        except Exception as e:
            return bad_request(request , e)

        outputserializer = self.OTPOutSerailizer(data = response)
        outputserializer.is_valid()

        return Response(outputserializer.data , status=HTTP_201_CREATED)
        
from .interface import (
    send_otp_sms ,     
)


class SmsOtpSendApi(BaseOtpSendApi):
    
    class OTPInSerailizer(serializers.Serializer):
        phone = serializers.CharField(
            validators = [PhoneValidator('Is Not Valid Phone','no_valid_code')]
        )
    class OTPOutSerailizer(serializers.Serializer):
        token = serializers.CharField()
        rate_limite = serializers.IntegerField()

    def otp_process(self, data, **kwargs):
        token  = send_otp_sms(phone_number=data['phone'])
        return {
            'token':token , 
        }
    def post(self, request, **kwargs):
        return super().post(request, **kwargs)
    