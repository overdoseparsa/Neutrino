from typing_extensions import override
from neutrino.account.SignService.api import USER
from typing import AbstractSet
from django.contrib.auth.models import AbstractUser
from neutrino.otp.interface import BaseVerifyOtp, IsVerifyedOTP
from abc import ABC , abstractmethod
from neutrino.core.provider import RequestsLimitationProvider , BaseRequestValidator
from neutrino.account.auth_sign.service import user
from django.contrib.auth import get_user_model
import logging
from config.django.test import PASSWORD_HASHERS

USER_ = get_user_model()

class BaseFactoyGetuser(ABC):

    def __init__(self , **kwargs):
        assert kwargs.get('query')  , "you have to add quey site "
        self.query = kwargs.get('query')
    @abstractmethod
    def get_user_context(self)->AbstractUser:
        """
        my logic if i want to find a email or phone with hast
        >>> username = lambda  :  get_hast_username(query['email']):...
        >>> Username = username('parsakhakiy@gmail.com')
        >>> USER.objects.get(
        username = Username
        )
        againse ....
        >>> Username.object.get(email="parsakhakiy@gmail.com")


        this is my logic the way off getting the AbstractUser
        """
        pass # logic

class SimpleOrmFactroy(BaseFactoyGetuser):
    def get_user_context(self)->AbstractUser:
        return USER_.objects.get(**{self.query})

class  HashFinedFactory(BaseFactoyGetuser):
    # for pyload email for phone number
    # using hash in database
    def get_user_context(self)->AbstractUser:
        pass  # TODO adding the hash


class BaseOtpLoginService(ABC): # abstact
    """
    why is use duplicate code here
    and i dont specify abstract
    becuase if want to change my service app
    be adaptable with this stauts and be scalable ...:)
    """
    otp_validator = IsVerifyedOTP
    service_validator = RequestsLimitationProvider
    loggin_logger = logging.getLogger('LogginApilogs')
    @property
    def Loggin_Logger_(self):
        assert isinstance(self.loggin_logger , logging.Logger) , "The logger must be instance from logger"
        return self.loggin_logger
    @property
    def Service_Validator(self):
        assert issubclass(self.service_validator , BaseRequestValidator) , 'The request_validator must be ontnce from BaseRequestValidator'
        return self.service_validator

    @property
    def Cli_otp(self):
        assert issubclass(self.otp_validator , BaseVerifyOtp) , 'The interface Verify otp musb be isubclass from BaseVerifyOtp'
        # assert (hasattr(self.otp_validator , '_validate') and hasattr(self.otp_validator , '_remove_token')   ) , """interface of BaseVerifyOtp subclass  must have _validate , _remove_token"""
        return self.otp_validator

    def __init__(self , token , request): # handeler = email , phone
        self.token = token
        self.request = request
        self.run_validation() # error | continue


    def run_validation_otp(self):
        self.cli_interface = self.Cli_otp(self.token)
        self.cli_interface.validate(raise_expection=True) # error
        # after validation remove otp
        self.context_data = self.cli_interface.get_the_context()
        self.cli_interface.remove_token() # if token is exits

    def run_validation(self):
        self.run_validation_otp()
        self.Service_Validator(self.request)

    user_interface_factory = BaseFactoyGetuser
    @property
    def get_user_factory(self):
        assert issubclass(self.user_interface_factory , BaseFactoyGetuser) , "User factory interface must be subclass from  BaseFactoryGetUser"
        return self.user_interface_factory

    @override
    def handel_user(self)->None: # factroy

        """
        if i want
        i can just return user
        and dont use the factory_handell
        >>> class MyOtpLoggin(BaseOtpLoginService):
            ... def handel_user(self)->AbstractUser:
                    self.user = user.object.get(phone = self.context_data['phone'])
            ```
                it is adaptable
                if i want  to just return user and
                dont neet should create factory_method
                HINT > the handle can`t be paradim without Factory user interface
                ... and just set  _user
            ```

        """

        _user_factory = get_user_factory(
        )  #INIT must

class PhoneOtpLoggin(BaseOtpLoginService):

    def handel_user(self) -> None: #
        self.context_data.pop('time')
        self.__user_factory = self.get_user_factory(
            query = self.context_data
        )
        self.user = self.__user_factory.get_user_context()
        self.Loggin_Logger_.info(f'user is loggin with {self.context_data} from phone')


class EmailOtpLoggin(BaseOtpLoginService):
    def handel_user(self) -> None: #
        self.context_data.pop('time')
        self.__user_factory = self.get_user_factory(
            query = self.context_data
        )
        self.user = self.__user_factory.get_user_context()
        self.Loggin_Logger_.info(f'user is loggin with {self.context_data} from phone')

    @property
    def retrive_user(self)->AbstractUser:
        assert hasattr(self , 'user') , 'handel User must be called' ,
        return self.user
