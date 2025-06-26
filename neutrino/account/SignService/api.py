from rest_framework.views import APIView 
from rest_framework.status import HTTP_200_OK  
from rest_framework import serializers
from rest_framework.response import Response
from neutrino.account.validator import ValidationsAccount
from django.core.validators import MinLengthValidator , MaxLengthValidator
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from django.core.exceptions import ValidationError 
from django.http import HttpResponse , HttpRequest , HttpResponseForbidden 
import logging
from abc import abstractmethod
from rest_framework.exceptions import bad_request
from rest_framework.status import HTTP_200_OK
from django.urls import path

USER = get_user_model()
print(USER , 'model is' )
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class BaseSignAccountApi(
    APIView
):

    """
    This paradim of this strcture is like Otp app code 
    why i dont use the interface or whay am i  use it againt and dont create 
    t base structer for all api ? or deplicate design

    i decided it is better for sacableity off ap is i want to use this app or otp for 
    a nother envierment it probelty dont have access the base inter face 


    >>> class Baseapi:
    ... def post():
            ...
    ... def get_seraializer():
            ...

    >>> class opt(Baseapi):
    >>> class sign(Baseapi): 
    """  
    class SignOutputSerailizer(serializers.ModelSerializer):
        class Meta :
            model = get_user_model()
            fields = '__all__'
        # for JWT 


        """
        note we can use the a custom auth token 
        from this mehtod for be scabale in authentication 
        bur is rather to use jwt inthis seriailzer 
        """
        # validation 
        def add_jwt_context(self , username , password)->None:
            self.username , self.password = username , password
        
        def jwt_token(self , user): 
            jwt_intance = TokenObtainPairSerializer(data = {'username':self.username , 'password':self.password})
            jwt_intance.is_valid()
            print('the validated data is ' , jwt_intance.validated_data )
            return jwt_intance.validated_data

             
        token = serializers.SerializerMethodField('jwt_token')  
        

    class SignInputSerializer(serializers.Serializer):        
        token = serializers.CharField()
        username = serializers.CharField(
                    validators = [
                        MinLengthValidator(limit_value=10) , 
                        MaxLengthValidator(limit_value=100) , 
                        ValidationsAccount.username_validation 
                    ]  , 
        required = True
                )
        name = serializers.CharField(required = True)
        family = serializers.CharField(required = True)
        password = serializers.CharField(
                    validators = [
                        MinLengthValidator(limit_value=10) , 
                        MaxLengthValidator(limit_value=100)
                    ]  , 
                    required = True
                )
        confirm = serializers.CharField(
                    validators = [ 
                    MinLengthValidator(limit_value=10) , 
                    MaxLengthValidator(limit_value=100)
                    ] , 
                    required = True

                )
        

        def validate(self, attrs): # this is sign inn
                # check_the_username 
                # check the email 
                # check the phone number
            assert attrs.get('password') == attrs.get('confirm') , ('Dont Password match from server')
            return super().validate(attrs)

        

        
        
    InputSerializer =  SignInputSerializer
    OutputSerializer = SignOutputSerailizer

    @abstractmethod
    def sign_process(self , data ,  **kwargs):
        "impelemntted ,,,"
        
    @property
    def get_logger(self)->logging.Logger:
        assert isinstance(self.sign_logger , logging.Logger) , "the Sign api logger mus be instance from logger" 
        return  self.sign_logger    
      
    
    @property
    def get_input_serializer(self)->serializers.Serializer:
        return self.InputSerializer
    

    @property
    def get_output_serialzer(self)->serializers.Serializer:
        return self.OutputSerializer
    
    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self , request , **kwargs)->Response:
        self.get_logger.info(f'the pyload from sign Api is  requested is {self.request.POST} ' , )
        
        input_serailizer = self.get_input_serializer(data = request.POST) # property 
        try:
            input_serailizer.is_valid(raise_exception=True)
            response = self.sign_process(input_serailizer.data , request , **kwargs)
        except BaseException as e:
            print('InterNullERROR ' , e)
            return bad_request(request , e)

        
        outputserializer = self.get_output_serialzer(response)
        outputserializer.add_jwt_context(input_serailizer.data['username'] , input_serailizer.data['password'])

        print('out put is ')
        print('the_data is ' , outputserializer.data)
        print('the response is ' , response)
        return Response(data = outputserializer.data ,
                        status=HTTP_200_OK , )



from .service import SignAccountPhone


class PhoneSignAccount(BaseSignAccountApi):

    sign_logger = logging.getLogger('SignApilogs')
    def sign_process(self, data, request , **kwargs):
        print(
            'The data is from phone signapi' , data
        )

        sign_interface = SignAccountPhone(data,request)
        sign_interface.create_user()
        sign_interface.Create_Settigns()
        sign_interface.Create_NetworkProfile()
        user = sign_interface.retrive_user
        
        return user 
    

ROUAT_SIGN_API = path('sign/' , PhoneSignAccount.as_view() , name='Sign_api')






# # TODO this is from email service 
# class EmailsignAccount(BaseSignAccountApi):
#     pass
