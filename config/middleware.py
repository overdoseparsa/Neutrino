import logging 
from django.http import HttpRequest , HttpResponse


class LoggerMiddleware:

    logger_middleware = logging.getLogger('middlewarelogs')
    
    def __init__(self , get_response):

        self.get_response = get_response

    def __call__(self, request:HttpRequest)->HttpResponse:

        self.logger_middleware.info(f'incoming requests [{request.method}] <--> [{request.path}]')
        
        print(f'incoming requests [{request.method}] <--> [{request.path}]')
	    
        return self.get_response(request)
    
