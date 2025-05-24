from django.core.validators import(
EmailValidator ,
RegexValidator ,
)
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator , EmailValidator
from django.db import models

class BaseValidtorMixinCore:
    regex = ...
    def __init__(self , message:str|None=None , code :str = None):
        self.message = message if message else None
        self.code = code if code else None
    def __call__(self , values):
        self.check_validation(values)

    def check_validation(self , values):
        values_validator = RegexValidator(regex=self.regex , message=self.message,code=self.code) 
        values_validator(values)


class FileValidatoPentrate(
    BaseValidtorMixinCore
):
    regex = r"^[a-zA-Z0-9_-]+\.(jpg|jpeg|png|gif|webp|mp4|mov|avi|mkv|mp3|wav|flac|pdf|docx|txt|zip|rar)$"

# is not workning 
class PhoneValidator(BaseValidtorMixinCore):
    regex = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"

class SqInjectionSafeValidator(BaseValidtorMixinCore):
    regex = r'^[^"\';<>]*$'

class SqInjectionSafeValidatorPassword(BaseValidtorMixinCore):
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'





def no_Empty_validator(values):
    assert values , ValidationError("Empty Error Values")

class ValidationsAccount:
    username_validation = RegexValidator(
        regex = r'^(?=.*[A-Z])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]+$',
        message = '''
        Username must to have a Upperlowercase
        - Username must have
        - Username have a One SpeailCractor
        '''  ,
        code = 'Dont_access_username'
    )


    email_validation = EmailValidator(
        message = """
        have mail be confirmed from server
        """
         ,
        code = "invalid_mail" ,
    )
    phone_validation = PhoneValidator(
        message = '''
        - phone is not validate`t  
        '''  ,
        code ='Dont_access_username'
    )

    sql_injection_safe_validator = SqInjectionSafeValidator( # TODO save ip and more Header request
        message = """
        it is not good confor mation for injection 
        """ , 
        code = "sql_injection" 
    )
    sql_injection_safe_validator_password = SqInjectionSafeValidatorPassword(
        message = """
        not valid this is for injection 
        """ , 
        code = "sql_injection" 
    )
    NotEmpty = no_Empty_validator