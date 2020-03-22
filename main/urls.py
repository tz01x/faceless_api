from django.urls import path,include,reverse_lazy
from .views import  homeview
app_name='main'
urlpatterns = [
path('',homeview,name='homeview'),
]
