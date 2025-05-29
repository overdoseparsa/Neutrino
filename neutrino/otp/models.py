from django.db import models
class messageLog(models.Model):
    sender = models.CharField(max_length=1000)
    reciver = models.CharField(max_length=1000)
    subject = models.CharField(max_length=1000)
    message = models.TextField()
    time_send = models.DateTimeField(auto_now_add=True)
    class Meta :
        abstract =  True
    

    
class Mailsystem(messageLog):...

class SmsSystem(messageLog):...


