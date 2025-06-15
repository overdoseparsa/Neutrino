from django.http import  HttpResponseServerError
from neutrino.account.models import DefaultUser
from django.db.models import QuerySet
from .process import BaseQuerySetSerializer

class QueryParamSerialize(BaseQuerySetSerializer):
    model_base = DefaultUser

def filter_param_with_args(query_parsms:str)->tuple:
    Query_params = QueryParamSerialize(
        query_param = query_parsms
    )

    return Query_params.data



def GET_User_Info(request ,*args ,**kwargs)-> QuerySet[DefaultUser]:
    ''' This is for api Profile View Return the Object by id  '''
    primary_key_id = kwargs.get('id')

    assert primary_key_id , HttpResponseServerError('invalid QueryParams')
    if not request.query_params.get('fields'):
        pass
        content = DefaultUser.objects.get(
            id = primary_key_id
            )
        print('dont have prram and content is ' , content)
    else : 
        field_query = filter_param_with_args( 
                    request.query_params
                )
        
        content = DefaultUser.objects.only(*field_query).get(
            id = primary_key_id  
            )
        print('the content with fileds is '  , repr(content))
    return content

