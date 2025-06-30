from kavenegar import KavenegarAPI


class KavenegarProvider(KavenegarAPI):
    def Send_Message(self , subject  ,sender ,  receiver  ,  message):
        params = {'receptor':receiver , 
                'sender':sender , 
                'message':f'{subject}' +  f'\n {message}' 
                 }
        
        self.sms_send(params=params)
        # kavenegar logs 



class TestProvider:
    def Send_Message(self , subject  , receiver  ,sender , message):
        params ={'receptor':receiver , 
                 'sender':sender , 
                 'message':f'{subject}' +  f'\n {message}' 
                }
        print( 'sendng message' ,  params)

