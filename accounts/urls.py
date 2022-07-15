from django.urls import path
from . import views


appname='accounts'


urlpatterns=[
	path('',views.accounts_api,name='accounts_index'),
	path('user/create',views.AccountsAPIView.as_view(),name='accounts_api'),
	path('user/login',views.login_APIView,name='login'),
	path('user/details',views.getUserDetailsAPIView,name='user_details'),
	path('user/verify',views.VerifyUser.as_view(),name='verify_user'),
	# path('email/template/',views.CreateEmailTemaplateView.as_view(),name='create_email_template'),
	path('verified/mails',views.get_verified_users,name='get_verified_users')
]