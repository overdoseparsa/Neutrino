from django.contrib import admin
from .models import (
    DefaultUser , 
    UserSettings  , 
    Profile ,
    UserNetworkProfile
    
)
admin.site.register(DefaultUser)
admin.site.register(UserSettings)
admin.site.register(Profile)
admin.site.register(UserNetworkProfile)