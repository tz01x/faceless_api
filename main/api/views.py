from django.http import JsonResponse,HttpResponse,HttpResponseBadRequest
from rest_framework import status
from rest_framework.response import Response
import  json
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from user.api.utils import  decode_uid

@api_view(['GET'])
@permission_classes([])
def getusername(request):
    # data=[]
    try:
        uid=request.GET.get('uid',None)
            
        
    except:
         uid=request.data.get('uid')
         
            
    if uid is not None:
        user=decode_uid(uid)
        if user:

            return Response(data={'name':user.username},status=status.HTTP_200_OK)
    return Response(data={'details':"this user don't exist  "},status=status.HTTP_400_BAD_REQUEST)

from main.serializers import MyMessagesSerializer
from rest_framework import generics
from main.models import MyMessages,Message
@api_view(['GET'])
def MyMessagesView(request):
    qs=MyMessages.objects.getserializer_data()
    return Response(qs)

class MyMessagesView2(generics.ListCreateAPIView):
    queryset = MyMessages.objects.all()
    serializer_class = MyMessagesSerializer
    permission_classes = []

    def get_queryset(self):
        try:
            uid=self.request.GET.get('uid',None)
            
        
        except:
            uid=self.request.data.get('uid')
         
            
        if uid is None:
            #return empty set
            return []
        #
        user=decode_uid(uid)
        print(user)
        #
        #
        if user:
            qs=MyMessages.objects.all().filter(user=user)
            return qs
        else:
            # return empty set
            return []

        # raise ValueError


    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        # .filter(user=request.user)
        serializer = MyMessagesSerializer(queryset,many=True)
        return Response(serializer.data)
import json,io
@api_view(['POST'])
@permission_classes([])
def createMessage(request):
    uid=None
    text=None
    try:
        data=request.data
        print(data)
        # jdata=json.loads(data)
        # print(jdata)
        uid=data['uid']
        text=data['text']
        print(uid)
    except Exception as e:
        print(e)
        print('data was send as a from-data')
        uid=request.POST.get('uid',None)
        text=request.POST.get('text',None)
    finally:

        if uid is None:
            return Response({'detail':'Opps!, this link is invalid. Try a valid link '.title()},status=status.HTTP_403_FORBIDDEN)
        user=decode_uid(uid)
        if user is None:
            return Response({'detail':'this link is invalid. Try a valid link '.title()},status=status.HTTP_403_FORBIDDEN)

        msg=Message.objects.create(text=text)
        myMessages,c=MyMessages.objects.get_or_create(user=user)
        myMessages.messages.add(msg)
        return Response({'detail':'message send'},status=status.HTTP_201_CREATED)
