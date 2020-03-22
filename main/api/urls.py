from django.urls import path,include
from .views import (getusername,MyMessagesView,
                MyMessagesView2,createMessage)
urlpatterns = [
    path('getusername/',getusername),
    # path('myessages/',MyMessagesView.as_view())
    path('testmyessages/',MyMessagesView),
    path('sendmessage/',createMessage),
    path('messages/',MyMessagesView2.as_view()),
]
