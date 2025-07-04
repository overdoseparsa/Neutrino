from django.contrib import admin
from .models import  Post , Comment , Conection 
admin.site.register(
    (Post , Comment , Conection)
)