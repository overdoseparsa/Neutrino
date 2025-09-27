from django.urls import path
from .api import retrive_url, test_urls


urlpatterns = [
    test_urls , 
    retrive_url
]