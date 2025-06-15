from django.test import TestCase

from .ViewService.process  import  (check_regex ,
 BaseQuerySetSerializer) 
from neutrino.account.models import DefaultUser


def test_query_param():
    ''' This function is for testing ViewService procces and check BaseQuerySerializer '''
    class BaseUserQuery(BaseQuerySetSerializer):
        model_base = DefaultUser


    # one test 
    # init without query param 
    test_query_param = BaseUserQuery(query_param={'fields':'bio,username'})
    # test_query_param.run_validation()
    print('data from validation' , test_query_param.data)
    print('starting testing  Regex ...')
    print(  'check validation regix ',check_regex(
        r'^[a-zA-Z0-9_,]+$' , 'asdasd'
    ))
    print('ending testing  Regex')
#test_query_param()
