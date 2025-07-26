from django.http import HttpRequest
from neutrino.core.provider import  BaseRequestValidator
from abc import ABC , abstractmethod
from neutrino.post.models import Post
from django.db import transaction

import logging 



class BaseInterfaceQueryService(ABC): # stregety design pattrens 
    """
        HINT: This class is scalable for refactor if I want to add another type of getting query.

        Example:
            >>> class MyInterfaceQuery(BaseInterfaceQueryService):
            ...     def add_query(self, payload, user):
            ...         self._query = convert_to_sql(payload, user)
            ...     
            ...     def configure_service(self):
            ...         return Post.objects.raw(self._query)
            ...
            >>> self._query = 'SELECT * FROM POST WHERE user_id = user.id'

        This pattern allows adding another Query by subclassing.
        Note: This structure must have _query attribute.
        """
    
    def __init__(self , payload , user): # data 
        self.add_query(payload , user)
    
    @abstractmethod
    def add_query(self , payload , user)->None: # create Query
        """
            may be have altration in  columns name Not related from Api field I Can change here
        """
        self._query = {**payload}
        self._query['author'] = user.id


    
    @abstractmethod
    @transaction.atomic
    def configure_service(self)->object:... 

    





class CreatePostInterface(BaseInterfaceQueryService):

    def add_query(self, pyload):
        super().add_query(pyload)


    
    def configure_service(self): 
        # logger post from ... was creted  
        try : 
            return Post.objects.create(
                **self._query
            )

        except BaseException as E  :
            print(E)
            return False

from django.core.exceptions import ObjectDoesNotExist

class UpdatePostInterFace(BaseInterfaceQueryService):
    def __init__(self, pyload):
        super().__init__(pyload)
        assert 'pk' in pyload , "pk must be insert from pyload" # permission
        

    def configure_service(self)->object | bool:
        # a nother logic 
        try : 

            post_obj = Post.objects.get(**self._query)
        except ObjectDoesNotExist as obj_messge :
            print(obj_messge)
            return False

        except BaseException as E :
            print(E)
            return False






class PostStructer(ABC):
    request_provider = ...

    Query_Interface = ...
    loggin_post = ... 
    def __init__(self , request:HttpRequest , data):
        self.request = request 
        self.data = data 

        self.run_validation()

    @property 
    def get_request_proiver(self):
        assert issubclass(self.request_provider , BaseRequestValidator) , "request provicer must be instance from BaseRequestValidator"
    

    @property
    def get_query_interdface(self)->BaseInterfaceQueryService:
        assert issubclass(self.Query_Interface , BaseInterfaceQueryService) , "the query inter face must be subclass from BaseInterfaceQueryService"
        return self.Query_Interface
    @property
    def get_logger(self)->logging.Logger:
        assert isinstance(self.loggin_post , logging.Logger) , 'logging post must be instance from logger'
        return self.loggin_post



    def validate(self): 
        """
        HINT : if you have validation
        ... 
        """
        pass


    def run_validation(self):  
        """if i want to add valiation just override _validate"""

        self.request_provider(self.request)
        self.validate()




    @abstractmethod
    def configure_query(self):
        self.get_logger.info( 
            f"saving from Service {type(self).__name__} \'pyload\' {self.data} , \'user\' {self.request.user}"
        )
        
class CreatePostStructer(PostStructer):
    Query_Interface = CreatePostInterface
    loggin_post = logging.getLogger('Post_create_service')
    def configure_query(self):
        super().configure_query(self.data)  # here configure from server 

        interface = self.get_query_interdface(
            self.data , self.request.user
        )
        return interface.configure_service()







class UpdatePostStructure(PostStructer):
    Query_Interface = UpdatePostInterFace
    loggin_post = logging.getLogger('Post_update_service')
    def configure_query(self):
        super().configure_query(self.data)  # here configure from server 

        interface = self.get_query_interdface(
            self.data , self.request.user
        )
        return interface.configure_service()







