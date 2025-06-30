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
from django.test import TestCase
from unittest.mock import patch, MagicMock
from neutrino.account.LogginService.selector import PhoneOtpLoggin, USER_

class PhoneOtpLogginTest(TestCase):
    def setUp(self):
        self.user = USER_.objects.create(phone="09130000000", username="testuser")
        self.fake_request = MagicMock()
        self.token = "123456"

    @patch("neutrino.account.LogginService.selector.IsVerifyedOTP")
    @patch("neutrino.account.LogginService.selector.RequestsLimitationProvider")
    def test_handle_user_success(self, mock_request_limiter, mock_otp_validator):
        # پیکربندی mock برای OTP
        mock_validator_instance = mock_otp_validator.return_value
        mock_validator_instance.validate.return_value = None
        mock_validator_instance.get_the_context.return_value = {'phone': '09130000000'}

        # اجرای کلاس اصلی
        login_service = PhoneOtpLoggin(token=self.token, request=self.fake_request)
        login_service.handel_user()

        user = login_service.retricve_user()

        self.assertEqual(user.phone, self.user.phone)
        self.assertEqual(user.username, self.user.username)
