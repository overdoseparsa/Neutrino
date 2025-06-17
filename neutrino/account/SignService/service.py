from neutrio.core.provider import RequestsLimitationProvider
from django.http import HttpRequests
class SignAccount:
    request_validate_provider = RequestsLimitationProvider
    def get_request_provider(self , request)->object:
        return self.request_validate_provider(request)

        
    def __init__(self, data , request:HttpRequests)->None:
        self.data = data 
        self.request = request
        self.request_provider = self.get_request_provider(request) # with
        self.request.check_vaidation_request()
        # check_it_is_otp_for_creating user     
    def start_validation():
        # check it dose not exits phone email and 
        # check it is validatiion otp from number and email from otp 
        # check ip validation 
        # check user is not exist # hash 

    def create_user():
        pass 

    def add_singnal():
        pass    

    def add_to_the_graph_database():
        pass
    ... # log user was extendd 
    return User 

    # pass 

    
