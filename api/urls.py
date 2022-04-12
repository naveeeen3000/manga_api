from django.urls import path,include
from . import views


appname="api"


urlpatterns = [
    path("search/",views.searchView,name='search'),
    path("user/",views.AccountsAPIView.as_view(),name='accounts'),
    # path("user/login/"),
    
]
