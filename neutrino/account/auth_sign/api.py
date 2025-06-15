from rest_framework.views import APIView 
from rest_framework.status import HTTP_200_OK  
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.exceptions import bad_request
from neutrino.account.validator import ValidationsAccount
from django.core.validators import MinLengthValidator , MaxLengthValidator
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from django.core.exceptions import ValidationError 
from django.http import HttpResponse , HttpRequest , HttpResponseForbidden 
from .service import Create_user



class SignAccountApi(
    APIView
):
    
    class SignEmailSerializer(serializers.Serializer):

        email =  serializers.EmailField(
            required = True
        )
        username = serializers.CharField(
            validators = [
                MinLengthValidator(limit_value=10) , 
                MaxLengthValidator(limit_value=100) , 
                ValidationsAccount.username_validation 
            ]  , 
            required = True
        )
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
        def validate(self, attrs):
            assert attrs.get('password') == attrs.get('confirm') , HttpResponseForbidden('Dont Password match from server')
            return super().validate(attrs)
    

    class OutPutAccountSerailizer(serializers.ModelSerializer):
        class Meta :
            model = get_user_model()
            fields = '__all__'
    
    @extend_schema(request=SignEmailSerializer, responses=OutPutAccountSerailizer)
    def post(self,request:HttpRequest , *args ,**kwargs)->HttpResponse:
        serializer = self.SignEmailSerializer(data = self.request.POST)
        if not serializer.is_valid():
            raise APIException({
                'message': 'Validation failed',
                'errors': serializer.errors,
                'received_data': request.data  
            })
            

        user = Create_user(serializer.data)
        return Response(
            data= self.OutPutAccountSerailizer(user).data , 
            status= HTTP_200_OK , 
            content_type= request.headers.get('content-type')
            )
