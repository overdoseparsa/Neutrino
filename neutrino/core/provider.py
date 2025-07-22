from abc import ABC , abstractmethod
class BaseRequestValidator(ABC):
    def __init__(self , request):
        self._request = request
        self.configure()

    @abstractmethod
    def configure(self):
        "..."

        

class RequestsLimitationProvider(BaseRequestValidator):
    def __init__(self, request):
        super().__init__(request)


from django.core.validators import RegexValidator
import re 
# HINT : dependency inversion princile  

class ValidateBase(ABC):
    regex = r'(<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>)'
        
    @abstractmethod
    def validate(self):
        """validation here"""

class RegexDjangovalidation():

        # dependency injection 
    def __init__(self):
        self.__regex_validaor = RegexValidator(regex=self.regex , message="malicious scripts Xss revrence" , code="403" ,flags="Forbidden" )
        
    def validate(self, content):
        self.__regex_validaor(content)
    


class XssSecurityProvider(BaseRequestValidator): 
    # dependency injection 
    def configure(self):
        Regex_obj = RegexDjangovalidation()
        for key, value in self.request.POST.items():
            Regex_obj.validate(value)
  