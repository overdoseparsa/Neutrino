import rest_framework.serializers
from neutrino.core.provider import RequestsLimitationProvider , BaseRequestValidator
from neutrino.otp.interface import BaseVerifyOtp , IsVerifyedOTP
import logging
from django.conf import settings
from neutrino.account.models import UserSettings , UserNetworkProfile
from django.http import HttpRequest
from abc import ABC , abstractmethod
from django.contrib.auth import get_user_model
import rest_framework
rest_framework.serializers.Serializer

class BaseSignAccount(ABC): 
    service_validator = RequestsLimitationProvider
    sign_log = logging.getLogger('SignApilogs')
    otp_validator = IsVerifyedOTP
    
    @property
    def Service_Validator(self):
        assert issubclass(self.service_validator , BaseRequestValidator) , 'The request_validator must be ontnce from BaseRequestValidator'
        return self.service_validator
    
    @property
    def sign_logger(self):
        assert isinstance(self.sign_log , logging.Logger) , "The logger must be instance from logger"
        return self.sign_log 

    @property
    def Cli_otp(self):
        assert issubclass(self.otp_validator , BaseVerifyOtp) , 'The interface Verify otp musb be isubclass from BaseVerifyOtp'
        # assert (hasattr(self.otp_validator , '_validate') and hasattr(self.otp_validator , '_remove_token')   ) , """interface of BaseVerifyOtp subclass  must have _validate , _remove_token"""
        return self.otp_validator
    

    def validation_otp_token(self , token):
        print('the token is ' , token)        
        self.cil_otp_interface = self.Cli_otp(token)    
        self.cil_otp_interface.validate(raise_expection=True)
        self.otp_context = self.cil_otp_interface.get_the_context()
        # self.cil_otp_interface.remove_token()
        


    def __init__(self ,data, request:HttpRequest ,*args,**kwargs)->None:
  


        # TODO we will model manager 
        # self.user = self.USER_model.Auth.SignUser(
        #     data
        # )
    

        self.request = request
        self.data = data
        self.run_validation(data, self.request)
        

    @abstractmethod
    def create_user(self)->None:
        self.sign_logger.info(f"""
            the {self.user.username} was added in {self.user.username}
            """)


    def run_validation(self , data , request:HttpRequest)->None:
        """
            Hint : you can overide validation 
            and altration or impelment a distinct Paradim
            why am i dont use a nother class from OTP validation 
            the creater off user it depends to the otp verfiacation 


            
            I don't want these two classes to be separate so that every developer knows that this is dependent on OTP.
            After the SRP rule, 
            I don't use SOLID principles for OTP because I don't want to extend it further depending on the user.

            >>> class OtpVaolidatorUser:
                    otp_validator = IsVerifyedOTP 

                    @property
                    def Cli_otp(self):
                        assert issubclass(self.otp_validator , BaseVerifyOtp) , 'The interface Verify otp musb be isubclass from BaseVerifyOtp'
                        # assert (hasattr(self.otp_validator , '_validate') and hasattr(self.otp_validator , '_remove_token')   ) , 
 
 
        # this is Sign User Not just create user ... 
        
        """
        
        self.validation_otp_token(data.get('token'))
        self.Service_Validator(request)
        # ... 

    def Create_Settigns(self) -> None:
        assert hasattr(self , 'user')  , 'The user have to created befor'

        UserSettings.objects.create(
            user = self.user  ,
        )
        self.sign_logger.info('The Settings   was add  ')

    def Create_NetworkProfile(self):
        assert hasattr(self , 'user')  , 'The user have to created befor'

        UserNetworkProfile.objects.create(
            user = self.user , 
            ipv4_address = self.request.META.get('REMOTE_ADDR') , # TODO 
            # last_known_ip = self.request.META.get('IP_ADDRES') # Here we can get from reverse proxy Traefik middle ware 
            first_seen  = self.otp_context['time']
        )
        self.sign_logger.info('The User was add from ')
    
    @property
    def retrive_user(self):
        assert hasattr(self , 'user')  , 'The user have to created befor'
        return self.user 



class SignAccountPhone(BaseSignAccount):
        

        """
        ```
        i use this design because i want if my
        pardaim of getting user will change i get
        it is adptabe with 
        ```

        >>> class SignAccount():
            ... def __init__(self, data, request, *args, **kwargs):
            ... super().__init__(data, request, *args, **kwargs)
            ... self.user = settings.my_manger.create(
                ... 
            )

            


        or if i want to add a new method 

        
        
        >>> class SignAccount():
            ... def __init__(self, data, request, *args, **kwargs):
            ...     super().__init__(data, request, *args, **kwargs)
                    self.add_to_grath_database(self)
            ... def add_to_grath_database(self):
                # logic 

                        
        # this is my Paradim :)
        """

        #TODO add gratph Nde To The gratph Database 
        def create_user(self)->None:
            print('creating useer .,,,,,,')
            """
            this is for your logic to create user 
            >>> class MySignLogic(BaseSignAccount):
                ... def create_user(self)->None:
                        self.user = ...
                        # logic for create ing user 

                        
                                                """
            self.user = get_user_model().objects.create(
                username = self.data.get('username') , 
                first_name = self.data.get('name') , 
                last_name = self.data.get('family') , 
                read_receipts = 1 ,
                phone = self.otp_context['phone'] , 
            )
            print('befor passwoeding'  , self.data.get('password') , type(self.data.get('password')))
            self.user.set_password(self.data.get('password'))
            self.user.save()
            print('userwas craeted and setted pawwrod ')
            return super().create_user()
            