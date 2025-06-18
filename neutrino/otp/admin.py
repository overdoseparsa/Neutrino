from django.contrib import admin

# Register your models here.
from .models import TESTMODELOTP , Mailsystem , SmsSystem
# class RegisterModel():
#     def __init__(self , *args):
#         for arg in args:
#             admin.site.register(
#             arg
#             )


# RegisterModel(
#     TESTMODELOTP , Mailsystem , SmsSystem
# 
admin.site.register((TESTMODELOTP , Mailsystem , SmsSystem))