from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.request import Request
from rest_framework.throttling import SimpleRateThrottle
from rest_framework import serializers 
from rest_framework.status import HTTP_200_OK

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated
from .selector import get_username_info , InfoProfileUser 

from drf_spectacular.utils import extend_schema , OpenApiParameter



from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class PageDetailsApi(APIView):
    # no need auth it can be auth user bot must be in system 

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model  = InfoProfileUser
            fields = "__all__"



    
    # throttle_classes = [SimpleRateThrottle]
    permission_classes = [IsAuthenticated]
    input_serializer = UserSerializer
    @property
    def get_input_serializer(self):return self.input_serializer
    @method_decorator(
        cache_page(60 * 60 * 2)
    )
    @extend_schema(
        responses=input_serializer , 
        parameters=[
        OpenApiParameter(
            name='username',
            type=str,
            location=OpenApiParameter.PATH,
            description='Username of the account to retrieve details'
            ) , 

        ]
    )
    def get(self , request:Request , **kwargs)->Response:
        info = kwargs.get('username')
        response = get_username_info(
            info 
        )  


        serializer  = self.get_input_serializer(
            data = response
        )
        return Response(
            serializer.data , status=HTTP_200_OK , 

        )
from django.urls import path 

PAGE_DETAILS_API = path(
    'Details/<str:username>/' , PageDetailsApi.as_view() , name='account_details'
)
