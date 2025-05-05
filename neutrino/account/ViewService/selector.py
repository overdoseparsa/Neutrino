from django.http import  HttpResponseServerError
from neutrino.account.models import DefaultUser
from django.db.models import QuerySet

def GET_User_Info(request ,*args ,**kwargs)-> QuerySet[DefaultUser]:
    #Show_The_account_Profile
    primary_key_id = request.query_params.get('id') if request.query_params.get('id') else args[0] if args  else kwargs.get('id') if kwargs.get('id') else None
    assert primary_key_id , HttpResponseServerError('invalid QueryParams')
    content = DefaultUser.objects.get(
        id = primary_key_id
        )
    print('content' , content)
    return content
