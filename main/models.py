from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MyMessagesManager(models.Manager):
    def getserializer_data(self):
        qs=self.get_queryset()
        return [i.aserializer() for i in qs]


class MyMessages(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    messages=models.ManyToManyField('Message',blank=True,null=True)
    create=models.DateTimeField(auto_now=True)
    objects=MyMessagesManager()
    # def __str__(self):
    #     return self.user.username
    def aserializer(self):
        messages=self.messages.all()
        return {
        'user':self.user.username,
        'messages':[m.aserializer() for m in messages],
        }

class MessageManager(models.Manager):
    def getAllSeriallizeData(self):

        qs=self.get_queryset()
        # if user:
        #     qs=qs.filter()
        return [item.aserializer() for item in qs]


class Message(models.Model):
                        #verbos_name , max_length
    text=models.CharField('message',max_length=500)
    create=models.DateTimeField(auto_now_add=True)
    objects=MessageManager()
    # auto_now_add - updates the value with the time and date of creation of record.
    def aserializer(self):
        return {
        'text':self.text,
        'create':str(self.create.date())
        }
    class Meta:
        ordering = ['-id']
