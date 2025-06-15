from abc import ABC, abstractmethod
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
import logging

# TODO instead of Validation use pydanic for some validation 


class InputModelError(Exception):...

class BaseSendMessage(ABC): # TODO have altration from asyncio  
    logger = ...
    log_model = ...
    def __init__(self, sender, receiver, message, subject, **kwargs)->None:
        self._sender = sender
        self._message = message
        self._subject = subject
        self._receiver = receiver
        self._init_logger = self._validate_logger()
        super().__init__(**kwargs) 

    def _log_progress(self)->None:
        log_model = self._validate_log_model()
        log_model.objects.create(
            subject=self.subject,
            message=self.message,
            sender=self.sender,
            receiver=self.receiver
        )

        self._init_logger.info(f'{str(self)} sent from {self.sender} to {self.receiver} at {timezone.now()}')
    
    
    def _validate_log_model(self)->model.Model | None:
        if not self.log_model or not issubclass(self.log_model, models.Model):
            raise InputModelError("log_model must be a Django Model subclass")
        return self.log_model

    def _validate_logger(self)->logging.Logger | None:
        if not self.logger or not issubclass(self.logger , logging.Logger) : 
            raise InputModelError("logger attr must be a Logger subcclass")
        return self.logger
    @classmethod
    @abstractmethod
    def send_group_message(cls):
        """Send message to a group of recipients"""
        pass

    @abstractmethod
    def send_message(self):
        """Send the message"""
        pass

    @property
    def message(self):
        return self._message
    
    @property
    def receiver(self): 
        return self._receiver.strip()
    
    @property
    def sender(self):
        return self._sender.strip()
    
    @property
    def subject(self):
        return self._subject.strip()

class DjangoEmailService(BaseSendMessage):
    log_model = None  # Should be set to a Django model for logging
    send_mail_structre = send_mail # Note : this is from django 
    def __init__(self, sender, receiver, message, subject, **kwargs):
        super().__init__(sender, receiver, message, subject, **kwargs)
        self.email_data = (
            self.subject,
            self.message,
            self.sender,
            [self.receiver],
        )
        # self._init_logger = self._validate_logger()

    def send_message(self)-> bool | None :

        try:
            self._init_logger.info("Email send be sucssesed from server ")
            self.send_mail(*self.email_data, fail_silently=False) # properrtu
            self._log_progress()
            return True
        except Exception as e:
            self._init_logger.error(f'Failed to send email from server: {str(e)}')
            return False
        

    def send_mail(self , *args,**kwargs):
        self.send_mail_structre(*args,**kwargs)



class SmsDjangoService(BaseSendMessage): # TODO must be use internull asyncio here
    '''
    >>> from ascynio 
    # we have to use api from system call 
    '''  
    sms_provider = ...
    
    def __init__(self, sender, receiver, message, subject, **kwargs):
        super().__init__(sender, receiver, message, subject, **kwargs)


    def _sms_provider(self):
        assert self.sms_provider  , 'Must Be implemnt from sms'
        if hasattr(self.sms_provider , '_Send_Message') : 
            self._init_logger.CRITICAL(f'Sms provider Service Not working')
            raise SystemError('The provider from sms sending must implement from BaseSmsProvider')

        return self.sms_provider
    
    def send_message(self):
        try : 
            self.sms_provider.Send_Message(
                subject = self.subject , 
                sender = self.sender , 
                message = self.message ,  
            )
        except Exception as e :
            self._init_logger.error(f'Some Error To sending SMS \n {e}') 
            return False 
            

            
class FactorySendmessage(ABC):
    '''
        We use Factory method where client does not need to access BaseSendmessage directly and does not design it. 
        where cilent with interface here and 
        we prefer client not to know about complexity
        and if we want to add new structure we do not change main class
                ```
        >>> service =  FactorySendmessage()
            service.send_message(
            sender = ... , 
            revciver = ... , 
            subject = ... , 
            message = ...
            )
        ```
           if I need to add a nother class form my usage 
           example:
            ```python 
            >>> class YahooSendMeesage(BaseSendMessage):...
            >>> class FactroySendSmsYahoo():
                    def BackendMessageService():...

            >>> new_service = FactroySendSmsYahoo()
                new_service.BackendMessageService()
                # suagee here 
            ```
        
        
        
        ```

    '''
    def __init__(self, sender, receiver, message, subject):
        super().__init__()
        self._interface =  BaseSendMessage(sender, receiver, message, subject)
    @abstractmethod
    def BackendMessageService(self)->BaseSendMessage:
        ''' Factory Method  '''
        return self._interface 
    
class EmailFactroyMethod(FactorySendmessage):
    def __init__(self ,sender, receiver, message, subject):
        self._interface = DjangoEmailService(sender, receiver, message, subject)
        
    def BackendMessageService(self)->DjangoEmailService:
        return self._interface
    
    def send_message(self)-> bool: 
        service = self.BackendMessageService()
        status = service.send_message()
        return status
    
class SmsFactroyMethod(FactorySendmessage):
    def __init__(self ,provider ,sender, receiver, message, subject):
        class SmsService(SmsDjangoService):
            sms_provider = provider
        self._mail_interface = SmsService(sender, receiver, message, subject)
        
    def BackendMessageService(self)->SmsDjangoService:
        return self._interface
    
    def send_message(self)-> bool: 
        service = self.BackendMessageService()
        status = service.send_message()
        return status
    # this is factroy mehfot 