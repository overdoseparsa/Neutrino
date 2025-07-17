from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

_USER_model = get_user_model()
def Subscribe(
        request , 
):  # auth need 
    try :
        user = request.user 
        user_target = _USER_model.objects.get(username=request.POST.get('username'))
        
        assert user != user_target 
        user.connection.add(user_target)
        user_target.forward_connection.add(user)
        return user_target
        
        # TODO here we use celery in django 
    except ObjectDoesNotExist as E :
        return str(E)
    


from django.http import HttpRequest
def Unsibscribe(request:HttpRequest):
    try:
        user = request.user 
        user_target = _USER_model.objects.get(username=request.POST.get('username'))
        user.connection.remove(user_target) 
        user_target.forward_connection.remove(user)
        return user_target
    except ObjectDoesNotExist as E :
        return str(E)
    


def get_follower(user):
    return user.FOLLOWING.filter(to_defultuser_id = user.id)


def get_followeing(user):
    return user.FOLLOWING.filter(to_defultuser_id = user.id)


def count(query_set):return query_set.count()

# TEST 