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


class TESTMODELOTP(models.Model):
    token = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    attempet = models.SmallIntegerField()
    time_requested = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    code =models.CharField(max_length=10)

