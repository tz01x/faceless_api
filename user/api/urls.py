from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token
from .views import  loginApi,register
urlpatterns = [
    # Your URLs...
    # path('token/', obtain_jwt_token, name='token_obtain_pair'),
    path('token/', loginApi.as_view(), name='token'),
    path('token-refresh/',refresh_jwt_token, name='rtoken'),
    path('register/',register, name='signup'),
]
# $ curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}' http://localhost:8000/api-token-auth/



# $ curl -X POST -H "Content-Type: application/json" -d '{"token":"<EXISTING_TOKEN>"}' http://localhost:8000/api-token-refresh/

# $ curl -H "Authorization: JWT <your_token>" http://localhost:8000/protected-url/
