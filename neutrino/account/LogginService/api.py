from django.contrib.auth.models import AbstractUser
from django.contrib.auth  import get_user_model
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework_simplejwt.serializers import RefreshToken 
from rest_framework.response import Response
from rest_framework.exceptions import  bad_request
from rest_framework.status import HTTP_200_OK

from drf_spectacular.utils import extend_schema
from neutrino.account.SignService.api import SignOutputSerailizer



import logging
from abc import ABC , abstractmethod
import logging 
# TODO will change
class LogginOutputSerailizer(serializers.ModelSerializer):
    class Meta :
        model = get_user_model()
        fields = '__all__'
        # for JWT 


        """
        note we can use the a custom auth token 
        from this mehtod for be scabale in authentication 
        bur is rather to use jwt inthis seriailzer 
        """

    def jwt_token(self , user):
        refresh_token = RefreshToken.for_user(user)
        return {

            'access':str(refresh_token.access_token) , 
            'refresh':str(refresh_token)
        }
             
    token = serializers.SerializerMethodField('jwt_token')  
        

class BaseLoginApi(APIView , ABC):
    
    class InputLogginSerailizer(serializers.Serializer):
        token = serializers.CharField()
    
    InputSerailizer = InputLogginSerailizer
    OutputSerailizer = LogginOutputSerailizer

    
    loggin_logger = logging.getLogger('LogginApilogs')
    @abstractmethod
    def loggin_process(self , data ,  **kwargs)->AbstractUser:
        "impelemntted ,,,"
        
    @property
    def get_logger(self)->logging.Logger:
        assert isinstance(self.loggin_logger , logging.Logger) , "the Sign api logger mus be instance from logger" 
        return  self.loggin_logger    
      
    
    @property
    def get_input_serializer(self)->serializers.Serializer:
        return self.InputSerailizer
    

    @property
    def get_output_serialzer(self)->serializers.Serializer:
        return self.OutputSerailizer
    
    @extend_schema(request=InputSerailizer, responses=OutputSerailizer)
    def post(self , request , **kwargs)->Response:
        self.get_logger.info(f'the pyload from Loggin Api is  requested is {self.request.POST} ' , )
        
        input_serailizer = self.get_input_serializer(data = request.POST) # property 
        try:
            input_serailizer.is_valid(raise_exception=True)
            response = self.loggin_process(input_serailizer.data , request , **kwargs)
        except BaseException as e:
            print('InterNullERROR ' , e)
            return bad_request(request , e)
        
        outputserializer = self.get_output_serialzer(response)

        return Response(data = outputserializer.data ,
                        status=HTTP_200_OK , )



    
from .selector import PhoneOtpLoggin

from django.urls import path

class EmailOTPLoggin(BaseLoginApi): # TODO 
    """
    Hint this is otp link email not 
    this is jsut loggin with email  
    """
 
class PhoneOTPLoggin(BaseLoginApi):
        
    class InputLogginSerailizer(serializers.Serializer):
        token = serializers.CharField()
    
    InputSerailizer = InputLogginSerailizer
    OutputSerailizer = LogginOutputSerailizer

    def loggin_process(self, data, request ,  **kwargs)->AbstractUser:
        otp_phone_loggin  = PhoneOtpLoggin(data.get('token') , request)
        otp_phone_loggin.handel_user()
        return otp_phone_loggin.retricve_user
    @extend_schema(request=InputSerailizer, responses=OutputSerailizer)
    def post(self, request, **kwargs):
        return super().post(request, **kwargs)
LOGGIN_URLS_PATH = path('loggin/' , PhoneOTPLoggin.as_view() , name='Loggin')

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UserNameModelSerialier(LogginOutputSerailizer):
    token = None
    def jwt_token(self, user):
        return None 
class UsernameLoggin(TokenObtainPairView):
    class OutputJWYInternullSerializer(TokenObtainPairSerializer):
        def validate(self, attrs):
            all_data = super().validate(attrs)
            username_serializer = UserNameModelSerialier(self.user)
            print('self user from Username loggin is ' , self.user)
            all_data['user'] = username_serializer.data
            return all_data 
    _serializer_class = OutputJWYInternullSerializer

    extend_schema(request={'username':'' , "password":''} , responses={'User':{} , 'access':None ,'refresh':None})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
LOGGIN_USERNAME_API = path('loggin/username/' , UsernameLoggin.as_view() , name="username_loogin")


    
