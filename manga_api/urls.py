
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.db import models
from . import views
# from rest_framework.authtoken import views

urlpatterns = [
    # path('',include(router.urls)),
    path('api-auth',include('rest_framework.urls',namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('',views.IndexView.as_view(),name='index'),
    path('api/v1/',include("api.urls")),
    path('api-auth/', include('rest_framework.urls'))

]
