import  json
#django
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
#djangoRest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import jwt_response_payload_handler
from rest_framework.permissions import  AllowAny
#other
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# jwt_response_payload_handler = api_settings.JWT_PAYLOAD_GET_USER_ID_HANDLER

def hendel_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    r=jwt_response_payload_handler(token,user)
    return r


class loginApi(APIView):
    permission_classes=[AllowAny]
    def post(self, request):

        data=None
        username=None
        password=None
        jdata=request.data
        print(request.data)
        try:
            #if data send as a json forment
            data=json.loads(jdata)

            username=data['username']
            password=data['password']
            # print(username)
        except:
            username=jdata.get('username')
            password=jdata.get('password')
            # print(username,'cnt load ')
            # print('21')
        finally:
            if username and password:
                user=authenticate(request,username=username,password=password)
                print(user)
                # login(request,user)
                if user is None:

                    return Response("[{'details':'username and password incorrect'}]", status=status.HTTP_400_BAD_REQUEST)

                else:
                    # payload = jwt_payload_handler(user)
                    # token = jwt_encode_handler(payload)
                    # r=jwt_response_payload_handler(token,user)
                    r=hendel_token(user)
                    print(r)

                return Response(r, status=status.HTTP_200_OK)



            else:
                return Response({'details':'username and password incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'details':'username and password incorrect'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data=None
    username=None
    password=None
    jdata=request.data
    try:
        #if data send as a json forment
        data=json.loads(jdata)
        username=data['username']
        password=data['password']
        email=data['email']
        # print(username)
    except:
        username=jdata.get('username',None)
        password=jdata.get('password',None)
        email=jdata.get('email',None)
    finally:
        if username and password and email:
            t=User.objects.filter(email__exact=email)
            # print(t)
            if len(t)==0:
                t=User.objects.filter(username__exact=username)
                if(len(t)!=0):
                    return Response({'details':f"this username='{username}' is already taken"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

                user=User.objects.create_user(username=username, email=email,password=password)
                # user.set_password(password)
                user.save()
                # user=authenticate(password=password, username=user.username)
                login(request,user)
                # login()
                r=hendel_token(user)
                return Response(r,status=status.HTTP_201_CREATED)
            else:
                return Response({'details':f'this email=\'{email}\' is already taken '},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
