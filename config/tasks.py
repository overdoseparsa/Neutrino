from time import sleep
from celery import shared_task

from neutrino.account.models import DefaultUser
@shared_task
def notify_customers(message):
    """
    for user in DefaultUser.objects.all():
        send_notic(user)
    
    it better to use 
    the graph database or binary search tree neo4j to use 
    to keep the email username for notify 



    and it better task do when t the Load of server is down in the  current time
    like 4:am 
    like 3:am 
    or a customize time that Passengers Dont have altration or use service  
    """
    sleep(20)