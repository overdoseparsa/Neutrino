from django.shortcuts import render
# we have to use json Web Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK , HTTP_404_NOT_FOUND
from rest_framework import  fields, serializers
from rest_framework.request import Request
from neutrino.api.pagination import LimitOffsetPagination
from neutrino.account.ViewService.selector import GET_User_Info
from django.conf import settings
from django.http import HttpResponseServerError
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from django.http import JsonResponse
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
