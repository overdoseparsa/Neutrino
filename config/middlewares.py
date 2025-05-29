import logging 
from django.http import HttpRequest , HttpResponse


class LoggerMiddleware:
    logger = logging.getLogger('middlewarelogs')
    def __init__(self , get_response):
        self.get_response = get_response

    def __call__(self, request:HttpRequest)->HttpResponse:
        logging.INFO(f'incoming requests [{request.method}] <--> [{request.path}] ')
        return self.get_response
    
