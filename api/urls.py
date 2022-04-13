from django.urls import path,include
from . import views


appname="api"


urlpatterns = [
<<<<<<< HEAD
    path("search/",SearchAPIView.as_view(),name='search'),

=======
    path("search/",views.searchView,name='search'),
    path("user/",views.AccountsAPIView.as_view(),name='accounts'),
    # path("user/login/"),
    
>>>>>>> f1d63e5af8ee04e95ac4dcc554490f98ef11c6df
]
