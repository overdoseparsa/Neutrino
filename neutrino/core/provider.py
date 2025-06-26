class BaseRequestValidator():
    def __init__(self , request):
        print('this is from requst limitation')


class RequestsLimitationProvider(BaseRequestValidator):
    def __init__(self, request):
        super().__init__(request)



from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils import timezone
import datetime

user = get_user_model()


def Create_user(data): 
    return user.objects.create_user(
        username=data.get('username') , 
        email= data.get('email') , 
        password= data.get('password')
    )


# this is base Create Data
# def _check_validation_time_session(time_block_utils):
#     return  is_time_difference_less(time_block_utils , timezone.now() , datetime.timedelta(hours=3)  )
    
class UserCreateBase: # rate limite 
    'logic may be scable but is is the base simple logic'
    # redis 
    def __init__(self , data , request:HttpRequest , **kwargs) ->None:
        self.data = data   
        self._request = request 
        self.validate_request_session()
    
    def validate_request_session(self)->None: 
        '''This is important who try to login in our services'''
        if not self._request.session.session_key:  # TODO use redis here for better permfomance 
                self._request.session.create()

                self._request.session['pre_login_tracking'] = {
                    'ip': self._request.META.get('REMOTE_ADDR'),
                    'user_agent': self._request.META.get('HTTP_USER_AGENT'),
                    'first_seen': str(timezone.now()),
                    'last_time':None , 
                    'login_attempts': 0 ,
                    'is_prime_block':False , 
                    'time_block_utils':None
                }

        
        # else : 
        #     if self._request.session['pre_login_tracking']['is_prime_block']:
        #         if _check_validation_time_session(self._request.session['pre_login_tracking']['is_prime_block']):
        #             raise TimeSessionExpection('That attemped from This session time is not expired \' try later')  
        #         else : 
        #             self._request.session['pre_login_tracking']['is_prime_block'] = False
        #             self._request.session['pre_login_tracking']['time_block_utils'] = None                                              
        #     else :
        #         self.attempt = self._request.session['pre_login_tracking']



    def servicce_login():
        pass





# check session from server [*]
# using otp from server 
# validate otp 
# after validate create the user and return authtaction from JWT 
# after that send the emeil that u are loggin in to the this service 
# it is better to just use email for varifacation we can use phone 
      

