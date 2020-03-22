from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
# from phonenumber_field.modelfields import PhoneNumberField #<---
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    location = models.CharField(max_length=300, blank=True)
    phone = models.CharField(blank=True,max_length=16)

    email_confirmed = models.BooleanField(default=False)

    '''
    Installation
    pip install django-phonenumber-field
    pip install phonenumbers

    INSTALLED_APPS = [
    ...
    'phonenumber_field',
    ...
    ]
    from phonenumber_field.modelfields import PhoneNumberField
    from phonenumber_field.formfields import PhoneNumberField

    phone = PhoneNumberField(blank=True,help_text="plase enter your phone number",max_length=16)

    phone = PhoneNumberField(max_length=16, help_text='Contact phone number mast be 8 chareture')



    Internally, PhoneNumberField is based upon CharField and by default represents the number as a string of an international phonenumber in the database (e.g '+41524204242').

Representation can be set by PHONENUMBER_DB_FORMAT variable in django settings module. This variable must be one of 'E164', 'INTERNATIONAL', 'NATIONAL' or 'RFC3966'. Recommended is one of the globally meaningful formats 'E164', 'INTERNATIONAL' or 'RFC3966'. 'NATIONAL' format require to set up PHONENUMBER_DEFAULT_REGION variable.

The object returned is a PhoneNumber instance, not a string. If strings are used to initialize it, e.g. via MyModel(phone_number='+41524204242') or form handling, it has to be a phone number with country code.

    +[country code][number]x[extension]
    +12223334444x55

    Use the |phone template filter to attempt to display a formatted phone number from arbitrary text. Use the |raw_phone template filter to display the raw, un-formatted value.

    Use property .is_E164 to check if a PhoneNumber object is in E164 format.

    Also provided are .is_standard (E164 but with extensions allowed) and .is_usa
    '''

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
