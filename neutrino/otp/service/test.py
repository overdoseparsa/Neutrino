from .core import SmsDjangoService

from .TestMockClass import MockTestProvicer , MockLogger

class TestCasSmsDjango(SmsDjangoService):

    sms_provider = MockTestProvicer
    logger = MockLogger('name_test') 
    log_model = ... # TO Be None just show database ECHO 
    def _validate_logger(self):
        return self.logger
    def _validate_log_model(self):
        pass
    

    def send_message(self):
        print(
            'subject' ,self.subject,
            'message' ,self.message,
            'sender' ,self.sender,
            'receiver' ,self.receiver,
        ) # TODO Create the internall  SMPP protocoll for testing 

        return super().send_message()
    

from unittest.mock import MagicMock

def send_message_simlit(self):
    print("sending_email_message")

def test_message_Django():
    SMS_magic_class = TestCasSmsDjango()
    
    
 

    service = SMS_magic_class(
                sender='0912...',
                receiver='0913...',
                message='test',
                subject='test'
    )
    pass