#from django.shortcuts import render
# we have to use json Web Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK , HTTP_201_CREATED , 
                                    HTTP_404_NOT_FOUND ,
                                      HTTP_400_BAD_REQUEST)
from rest_framework import  fields, serializers
from rest_framework.request import Request
from neutrino.api.pagination import LimitOffsetPagination
from neutrino.account.ViewService.selector import GET_User_Info
from django.conf import settings
from django.http import (HttpResponseServerError 
                        , HttpResponse  ,
                        JsonResponse , 
                        HttpRequest)
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from neutrino.account.validator import ValidationsAccount
from neutrino.account.ViewService.service import create_account , Update_account
'/account/<int:id>/?=base_query_dict'
class ProfileViewApi(APIView):
    """ Simple Api view for profile """

    class Pagination(LimitOffsetPagination):
        default_limit = 15

    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = '__all__'

    extend_schema(responses=OutPutSerializer)
    def get(self , request , *args , **kwargs):
        # TODO add The permision and auth to User model
        query = GET_User_Info(request  ,*args , **kwargs )

        serializer = self.OutPutSerializer(query)
        return Response(
                    serializer.data , status = HTTP_200_OK
                )




class CreateAccountApiView(APIView):
    class InputSeralizer(serializers.Serializer):
    # فیلدهای دلخواه تعریف میکنیم
        username = serializers.CharField(
            max_length=150  ,
            required = True  , 
            validators=[
            UnicodeUsernameValidator() , 
            ValidationsAccount.NotEmpty , 
            ] 
            )
        email = serializers.EmailField(
            validators=[
            ValidationsAccount.email_validation ,
            ValidationsAccount.NotEmpty 
            ] 
        )
        date_create_account = serializers.DateTimeField(
            default = serializers.CreateOnlyDefault(timezone.now)  , read_only=True
        )
        phone = serializers.CharField(
            validators=[
            ValidationsAccount.phone_validation ,
            ] 
        )
        password = serializers.CharField(
            validators=[
            ValidationsAccount.sql_injection_safe_validator ,
            ]         )

        gender = serializers.DateTimeField()
        read_receipts = serializers.BooleanField()

    # create the and return data 
    
    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = [
            'username',
            'email',
            'phone',
            'gender',
            'status',
            'about',
            'is_pro_user',
            'is_limited',
            'read_receipts',
            'date_joined',
            'last_login',   
        ]

    def post(self , request , *args , **kwargs):
        serializer = self.InputSeralizer(
            request.POST 
        )
             
        serializer.is_valid(
                raise_exception=True
            )

        account_object = create_account(serializer.data)

        return Response(
            self.OutPutSerializer(
               account_object
            ).data , status=HTTP_200_OK
        )    

# send the json File to the server 
# TODO‌ for letter 
#  full upgradde 
class UpdateProfileViews(APIView):
    class InputSerailizer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = [
                'gender' , 
                'status' , 
                'about' , 
                'bio'
            ] 
            
        def update(self, instance, validated_data):  
            '''dont want to internall logic ''' 

    class OutPutSerializer(serializers.ModelField):
        class Meta:
            model = get_user_model()
            fields = '__all__' 

    def put(self ,request:HttpRequest , *args , **kw): # primary id TODO‌ we change primary next 
        input_serializer = self.InputSerailizer(data  = request.POST)
        input_serializer.is_valid(raise_exception=True)
        instance = Update_account(
            input_serializer.data , kw 
        )
        return Response(
            data= self.InputSerailizer(instance).data , status=HTTP_200_OK
        )

# registery 