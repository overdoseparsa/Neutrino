from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.request import Request
from rest_framework.throttling import SimpleRateThrottle
from rest_framework import serializers 
from rest_framework.status import HTTP_200_OK , HTTP_400_BAD_REQUEST

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



from rest_framework.decorators import api_view, throttle_classes , authentication_classes 
from rest_framework.throttling import UserRateThrottle 
from rest_framework_simplejwt.authentication import JWTAuthentication


from rest_framework.throttling import UserRateThrottle

class OnceHPerDayUserThrottle(UserRateThrottle): # TODO adding the customize thrrorle 
    rate = '100/day'


from .service import Subscribe , Unsibscribe
@extend_schema(request={'username':'Parsa'})
@throttle_classes(OnceHPerDayUserThrottle)
@authentication_classes(JWTAuthentication)
@api_view(http_method_names=['POST']) # send username in POST  
def Subscribe_user(request:Request)->Response:
    try : 
        Subscribe(request)
        return Response(data={"status":"Ok"} , status=HTTP_200_OK)
    except BaseException as E :
        return Response(data={f"status":"Not Complete {E}"} , status=HTTP_400_BAD_REQUEST)


SUBSCRIBE_API_PATH = path(
    'subscribe' , Subscribe_user, name='subscribe'
)

@extend_schema(request={'username':'Parsa'})
@throttle_classes(OnceHPerDayUserThrottle)
@authentication_classes(JWTAuthentication)
@api_view(http_method_names=['POST']) # send username in POST 
def UnSubscribe_user(request:Request)->Response:
    try : 
        Unsibscribe(request)
        return Response(data={"status":"Ok"} , status=HTTP_200_OK)
    except BaseException as E :
        return Response(data={f"status":"Not Complete {E}"} , status=HTTP_400_BAD_REQUEST)

UNSUBSCRIBE_API_PATH = path(
    'unsubscribe' , UnSubscribe_user, name='unsubscribe'
)
