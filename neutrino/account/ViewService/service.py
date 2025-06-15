from django.db.models import QuerySet
from neutrino.account.models import DefaultUser

def create_account(data:dict)-> QuerySet : 
    return DefaultUser.objects.create_user(
        username= data['username'] , 
        email= data['email'] , 
        password = data['password'] , 
    )

def Update_account(data , kwargs):
    inctance = DefaultUser.objects.get()

# inhertancce and desion pattrens 
