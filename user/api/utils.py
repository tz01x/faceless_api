from django.conf import  settings
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils import  timezone
import  io
from django.contrib.auth.models import User

expTime=settings.JWT_AUTH['JWT_EXPIRATION_DELTA']
def jwt_response_payload_handler(token, user=None, request=None):
    user_str=str(user.id)+','+user.username
    return {
        'token': token,
        'user':{'username':user.username,'uid':urlsafe_base64_encode(user_str.encode())},
        'expire':timezone.now().date()+expTime,
    }
# Mix1c2Vy

def decode_uid(uid):
    '''

    '''
    try:
        
        byte_str=urlsafe_base64_decode(uid)
                        #'id,username'
        u=byte_str.decode().split(',')
        user=User.objects.filter(username=u[1],id=u[0])[0]
        if user:
            return user
    except:
        return None
    # return {'id':u[0],'username':u[1]}
