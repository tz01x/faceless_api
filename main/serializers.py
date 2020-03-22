from rest_framework import serializers
from .models import  MyMessages,Message
from django.contrib.auth.models import User

class messageSerializer(serializers.ModelSerializer):
    create= serializers.DateTimeField(format="%I:%M:%S %p %d-%m-%Y", required=False, read_only=True)
    class Meta:
        model=Message
        fields=['text','id','create']
        read_only_fields = ['id']
class UserS(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username']

class StringSerializer(serializers.StringRelatedField):

    def to_internal_value(self,value):
        return value


class MyMessagesSerializer(serializers.ModelSerializer):
    messages=messageSerializer(many=True)
    user=StringSerializer()
    # messages = StringSerializer(many=True)
    class Meta:
        model = MyMessages
        fields=('id','user','messages')
        # read_only_fields = ['user',]?
# from main.models import MyMessages
# from main.serializers import MyMessagesSerializer
# qs=MyMessages.objects.all()
