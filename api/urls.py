from django.urls import path
from .views import SearchAPIView
appname="api"


urlpatterns = [
    path("search",SearchAPIView.as_view(),name='search'),

]
