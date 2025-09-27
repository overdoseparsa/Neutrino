from rest_framework.views import APIView
from rest_framework import serializers 
from rest_framework.response import Response
from rest_framework.exceptions import bad_request
from rest_framework.status import HTTP_200_OK , HTTP_400_BAD_REQUEST


from rest_framework_simplejwt.authentication import JWTAuthentication

from django.urls import path 
from neutrino.post.models import Post
from django.http import HttpRequest , HttpResponse

from drf_spectacular.utils import extend_schema
class BasePostApiView(APIView):
	# permission_class = [JWTAuthentication]

	# permission_class = [JWTAuthentication]
	authentication_classes = [JWTAuthentication]
	class OutputPostSerializer(serializers.ModelSerializer): # Creatte and Update 
		class Meta:
			model = Post
			fields = ('title' , 'content')





	POST_OUTPUT_SERIALIZER = OutputPostSerializer
	@property
	def get_api_output_serializer(self):
		assert issubclass(self.POST_OUTPUT_SERIALIZER , serializers.Serializer) , 'POST_OUTPUT_SERIALIZER must be instance from Serializer'
		return	self.POST_OUTPUT_SERIALIZER
	
	@classmethod
	def get_output_serializer(cls):
		return cls.POST_OUTPUT_SERIALIZER

	def post(self , request:HttpRequest)-> HttpResponse: 
		"implement ... " 
		raise Exception('you must to Emplement')

	def get(self , request:HttpRequest)->HttpResponse:
		raise Exception('you must to Emplement')


	def update(self , request:HttpRequest)->HttpResponse:
		raise Exception('you must to Emplement')

	def delete(self , request:HttpRequest)->HttpResponse:
		raise Exception('you must to Emplement')



from .serializers import (
	InputPostCreateSerializer , 
	PutPostSerializer , 

	
) 
class PostApiSturcter(BasePostApiView):
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)



	PostApiSturcter = {
		"POST":InputPostCreateSerializer , 
		"PUT" : PutPostSerializer , 
	}
	
	
	class InputCreatePostSerializer(serializers.Serializer):
		title = serializers.CharField() 
		content = serializers.CharField()


	@classmethod
	def get_api_input_serializer(cls , method)->type:
		assert method in cls.PostApiSturcter , f"method have to be POST GET PUT DELETE not {method}"
		cls.__input_serializer = cls.PostApiSturcter[method] 
		assert issubclass(cls.__input_serializer[method] , serializers.Serializer)  , f"{cls.__input_serializer[method]} must be serializer"
		return cls.__input_serializer # here this is return serializer 
	
	def POST_ACTION(self , request , data,  **kwargs)->Post:
		pass


	def GET_ACTION(self , request, *args)->list[Post]: 
		"""
		Logic Here ... 
		"""

	def DELETE_ACTION(self)->None:
		pass

	def UPDATE_ACTION(self):
		pass



	def api_strutcure(self , request:HttpRequest , **kwargs):
		input_serializer = self.get_api_input_serializer(request.method)
		output_serializer = self.get_api_output_serializer
        # try:
        #     input_serializer.is_valid(raise_exception=True)
        #     response = self.sign_process(input_serailizer.data , request , **kwargs)
        # 	  nserializer_data = input_serializer(request.POST) 
		# except BaseException as e:
        #     print('InterNullERROR ' , e)
        #     return bad_request(request , e)
		input_data = input_serializer(data = request.data)
		print(input_data)

		
		input_data.is_valid(raise_exception=True)
		func_controller  = self.POST_ACTION if request.method == "POST" else (self.UPDATE_ACTION if request.method == 'PUT' else None)
		
		response = func_controller(request , input_data.data , **kwargs)

			
		output_data = output_serializer(
			response
		)
		
		return Response(
			output_data.data , status=HTTP_200_OK
		)
		

	@extend_schema(request=PostApiSturcter['POST'])
	def post(self, request):
		return self.api_strutcure(request)


	def update(self, request):
		return self.api_strutcure(request)	
	

	def get(self, request , *args):
		try : 
			response = self.GET_ACTION(request , *args) # Model[POST]
		except BaseException as e:
			return bad_request(request , e)

		output_serializer = self.get_api_output_serializer(response)
		return Response(
			output_serializer.data , status= HTTP_200_OK
		)

	def delete(self, request , *kwargs):
		try : 
			self.DELETE_ACTION(request , **kwargs)
		except BaseException as e:
			return bad_request(request , e)
		return Response(
			data= {'Action':'Done'} , status=HTTP_200_OK
		)

from neutrino.post.PostService.service import CreatePostStructer , UpdatePostStructure
from django.urls import path
from .models import Post
class ImplementtionAPiPost(PostApiSturcter):
	def POST_ACTION(self, request, data, **kwargs):
		print("user is " , request.user.id)
		return Post.objects.create(title =data.get('title') , content = data.get('content') , author = request.user)

	def GET_ACTION(self, request, *args):
		query = Post.objects.filter(author=request.user)
		from .serializers import OutputPostSerailizer
		serizlier = OutputPostSerailizer(query , many=True)

		return Response(serizlier.data , status=HTTP_200_OK)
	
	def get(self, request, *args):
		return self.GET_ACTION(request, *args)

test_urls = path('post/'  , ImplementtionAPiPost.as_view() , name="post_api")


class retriveAPiPost(PostApiSturcter):

	def GET_ACTION(self, request, *args):
		query = Post.objects.filter(author=request.user)
		from .serializers import OutputPostSerailizer
		serizlier = OutputPostSerailizer(query , many=True)

		return Response(serizlier.data , status=HTTP_200_OK)
	
retrive_url = path('posts/'  , retriveAPiPost.as_view() , name="post_api")

