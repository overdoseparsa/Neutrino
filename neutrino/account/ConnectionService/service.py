from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

_USER_model = get_user_model()
def Subscribe(
        request , username 
):  # auth need 
    try :
        user = request.user  
        user_target = _USER_model.objects.get(username='username')
        user.FOLLOWING.add(user_target)
        user_target.FOLLOWER.add(user)
        return user_target
        
        # TODO here we use celery in django 
    except ObjectDoesNotExist as E :
        return str(E)
    



def Unsibscribe(request , username):
    try:
        user = request.user 
        user_target = _USER_model.objects.get(username='username')
        user.FOLLOWING.remove(user_target) if user.FOLLOWING.filter(to_defultuser_id = user_target.id).exists() else None
        user_target.FOLLOWER.remove(user) if user.FOLLOWING.filter(to_defultuser_id = user.id).exists() else None

        return user_target
    except ObjectDoesNotExist as E :
        return str(E)
    

# cele