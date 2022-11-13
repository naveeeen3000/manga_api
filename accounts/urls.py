from django.urls import path
from . import views


appname='accounts'


urlpatterns=[
	path('user/create',views.CreateUserView.as_view(),name='accounts_api'),
	path('user/login',views.login_APIView,name='login'),
	path('user/details',views.getUserDetailsAPIView,name='user_details'),
]