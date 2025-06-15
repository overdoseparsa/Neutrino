from rest_framework.views import APIView
from rest_framework import serializers 
from rest_framework.status import (
HTTP_100_CONTINUE , HTTP_202_ACCEPTED , HTTP_400_BAD_REQUEST
)
from rest_framework.response import Response
from neutrino.account.validator import ValidationsAccount
from django.contrib.auth import get_user_model
from django.http import HttpRequest , HttpResponseBadRequest
from neutrino.account.registry.selector import  RegisterEmail  , RegisterUsername
from django.core.validators import MinValueValidator , MaxValueValidator

# class OTP 
# factory mehdo desigon pattern we use in This 
SERVICE_API='registery'
class ProfileRegister(APIView):
    class RegisterEmailSerailizer(serializers.Serializer):
        email =  serializers.EmailField()
        password = serializers.Serializer(
            validators = [ValidationsAccount.sql_injection_safe_validator_password , 
                         MinValueValidator(limit_value=10) , MaxValueValidator(limit_value=100)]
        )
        confirm = serializers.Serializer(
            validators = [ValidationsAccount.sql_injection_safe_validator_password , 
            MinValueValidator(limit_value=10) , MaxValueValidator(limit_value=100)]

        )
        def validate(self, attrs):
            return super().validate(attrs)
    

    class ProfileOutputRegister(serializers.ModelSerializer):
        class Meta : 
            model = get_user_model()  # return user model 
            fields = '__all__' # TODO it better to be email andjust user 
    def register_email(self, request:HttpRequest, **kwargs ):    
        serializer = self.InputProfileRegisterSerializerEmail(data= request.POST) 
        serializer.is_valid(raise_exception=True)
        user = RegisterUsername(serializer.data)
        return self.__Response_Logic(user)
    def register_username(self , request:HttpRequest  , *args , **kwargs)->Response:
        serializer = self.RegisterUsernameSerailizer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        user = RegisterUsername(serializer.data)
        return self.__Response_Logic(user)        
    def __Response_Logic(self , user)->Response:
        outputRegister_serializer = self.ProfileOutputRegister(user)
        return Response(
            outputRegister_serializer.data , status=HTTP_202_ACCEPTED
        )
    def dispatch(self, request, *args, **kwargs):
        assert request.META.get('RegisterType')
        type_request = request.META.get('RegisterType')
        if request.method =='POST' :
            if type_request == 'username':
                return self.register_username(request, *args, **kwargs)
            elif type_request == 'email':
                return self.register_email(request , *args , **kwargs)
            else :
                return HttpResponseBadRequest("Choice The registey Type ...")
        else : 
            return super().dispatch(request, *args, **kwargs)
            
