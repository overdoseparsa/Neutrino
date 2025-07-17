from celery import shared_task

from neutrino.otp.service.core import EmailFactroyMethod

from config.env import env 


@shared_task 
def send_email_for_hello(email_user):
    message = "hello well come to the neutrino"
    email_service = EmailFactroyMethod(
        sender=env("Email_PROVIDER" , "exsample@mail.com") , message=message ,subject="neutrino Social" , receiver=email_user
    )