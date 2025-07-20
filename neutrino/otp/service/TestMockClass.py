
from .SmsProvider import TestProvider



class MockTestProvicer(TestProvider):
    pass


from datetime import  datetime




class MockLogger:
    def __init__(self , name_test:str):
        self.name_test = name_test
    def action(self ,type_log , message ):
        print(f"The {type_log} log level {message} {datetime.now()}")

    def error(self , message):
        self.action(
            'ERROR'  , message
        )
    
    def info(self , message):
        self.action(
            'INFO'  , message
        )
    
    def critical(self , message):
        self.action(
            'CRITICAL'  , message
        )

    def __str__(self):
        return self.name_test