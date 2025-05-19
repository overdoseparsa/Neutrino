from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.core.validators import validate_ipv4_address , validate_ipv46_address
from neutrino.common.models import BaseModel
from django.contrib.auth.models import BaseUserManager as BUM
# auth
from .validator import (
    ValidationsAccount , FileValidatoPentrate , PhoneValidator
)
from .Field import (
    PhoneField
)
from django_countries.fields import CountryField

"""
Hint ...
whay i dont use AUTH_USER_MODEL from my Relateion
``` settings.py
from neutrino.account import models

AUTH_USER_MODEL = DefaultUser
```
ti
from neutrino.account import models
 is not finished it can defiend  the AUTH_USER_MODEL

"""




class BaseUserAccount(AbstractUser , BaseModel):

    class Gender(models.TextChoices):
        MAIL = '1' , 'mail'
        FEMAIL =  '0' , 'femail'
    gender = models.CharField(
        max_length=1 ,
        choices= Gender.choices
    )
    status = models.BooleanField(default=False)
    about = models.TextField(blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


    phone = PhoneField(
        max_length = 12 ,
        unique = True ,
        validators = [PhoneValidator]
        )

    is_pro_user = models.BooleanField(default=0)
    is_limited = models.BooleanField(default=0)
    connection = models.ForeignKey(
        'self' , on_delete=models.CASCADE , related_name = 'FOLLOWING' , null=True , blank=False
    )
    forward_connection = models.ForeignKey(
        'self' , on_delete=models.CASCADE , related_name = 'FOLLOWER' , null=True , blank=False
    )

    def __str__(self):
        return f'{self.username}'

    def __repr__(self):
        return f'{type(self).__name__}(**{self.__dict__!r})'

    def __unicode__(self):
        return self.email

    class Meta:
        abstract = True

    read_receipts = models.BooleanField(
        default=True,
    )


class UserSettings(BaseModel):
    class PrivacyChoices(models.TextChoices):
        PUBLIC = 'public', 'عمومی'
        FRIENDS = 'friends', 'دوستان'
        PRIVATE = 'private', 'خصوصی'

    class NotificationChoices(models.TextChoices):
        ALL = 'all', 'همه'
        MENTIONS = 'mentions', 'فقط منشن‌ها'
        NONE = 'none', 'هیچکدام'

    user = models.OneToOneField(
        'DefaultUser',
        on_delete=models.CASCADE,
        related_name='settings',
        verbose_name='کاربر'
    )

    # تنظیمات حریم خصوصی
    profile_visibility = models.CharField(
        max_length=10,
        choices=PrivacyChoices.choices,
        default=PrivacyChoices.PUBLIC,
        verbose_name='نمایش پروفایل'
    )
    last_seen_visibility = models.CharField(
        max_length=10,
        choices=PrivacyChoices.choices,
        default=PrivacyChoices.FRIENDS,
    )

    last_seen_profiles_day = models.ForeignKey(
        'DefaultUser' ,
        on_delete=models.CASCADE ,
        related_name ='SeenProfile' ,
        related_query_name="seenprofiles"
        )
    # تنظیمات نوتیفیکیشن
    message_notifications = models.CharField(
        max_length=10,
        choices=NotificationChoices.choices,
        default=NotificationChoices.ALL,
    )
    group_notifications = models.CharField(
        max_length=10,
        choices=NotificationChoices.choices,
        default=NotificationChoices.ALL,
    )
    sound_enabled = models.BooleanField(
        default=True,
    )

    # تنظیمات چت
    theme = models.CharField(
        max_length=20,
        default='light',
    )

    font_size = models.PositiveSmallIntegerField(
        default=14,
    )


    class Meta:
        verbose_name = 'setting Account'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return f'تنظیمات {self.user.username}'

# change manager 
class DefaultUser(BaseUserAccount):
    posts_count = models.PositiveIntegerField(default=0)
    subscriber_count = models.PositiveIntegerField(default=0)
    subscription_count = models.PositiveIntegerField(default=0)
    bio = models.CharField(max_length=1000, null=True, blank=True)


class UserNetworkProfile(BaseModel):
    user = models.OneToOneField(
                DefaultUser ,
                on_delete=models.CASCADE, related_name='network_profile'
    )

    # اطلاعات IP
    ipv4_address = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    ipv6_address = models.GenericIPAddressField(protocol='IPv6', null=True, blank=True)
    last_known_ip = models.GenericIPAddressField(protocol='both', null=True, blank=True)

    # اطلاعات موقعیت
    isp = models.CharField(max_length=100, blank=True, null=True)
    asn = models.CharField(max_length=20, blank=True, null=True)  # Autonomous System Number
    country = CountryField()

    # اطلاعات اتصال
    connection_type = models.CharField(max_length=20, blank=True, null=True,
                                      choices=[('wifi', 'WiFi'), ('mobile', 'Mobile'),
                                              ('ethernet', 'Ethernet'), ('other', 'Other')])
    bandwidth = models.PositiveIntegerField(blank=True, null=True)  # برحسب Mbps

    # امنیت
    is_vpn = models.BooleanField(default=False)
    is_proxy = models.BooleanField(default=False)
    is_tor = models.BooleanField(default=False)

    # زمان‌ها
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    # سایر اطلاعات
    user_agent = models.TextField(blank=True, null=True)
    device_type = models.CharField(max_length=50, blank=True, null=True)

    json_convert_data = models.JSONField(null=True , blank=False)


class Profile(BaseModel): # can `t update profile
    image_path = models.ImageField(
        validators=[
            FileValidatoPentrate ,
        ]
    )
    user =models.OneToOneField(
        DefaultUser,
        on_delete=models.DO_NOTHING  ,
        related_name="PROFILE" ,
        null=True ,
        blank=False
    )
    def __str__(self):
        return f'{self.user} : {self.created_at}'


