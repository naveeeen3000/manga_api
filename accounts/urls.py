from django.urls import path
from . import views


appname='accounts'


urlpatterns=[
	path('',views.accounts_api,name='accounts_index'),
	path('user/create',views.AccountsAPIView.as_view(),name='accounts_api'),
	path('user/login',views.login_APIView,name='login'),
	path('user/details',views.getUserDetailsAPIView,name='user_details'),
]