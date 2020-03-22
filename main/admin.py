from django.contrib import admin
from .models import  MyMessages,Message
# Register your models here.
admin.site.register(MyMessages)
admin.site.register(Message)
