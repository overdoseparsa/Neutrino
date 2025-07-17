from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DefaultUser
from .tasks import send_email_for_hello


@receiver(post_save, sender=DefaultUser)
def send_wellcom_mail(sender, instance, created, **kwargs):
    send_email_for_hello.delay(instance.email)