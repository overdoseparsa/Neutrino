from django.contrib import admin
from .models import (
    DefaultUser , 
    UserSettings  , 
    Profile ,
)
admin.site.register(DefaultUser)
admin.site.register(UserSettings)
admin.site.register(Profile)

