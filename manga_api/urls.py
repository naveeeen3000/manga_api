
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.db import models
from . import views
# from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.IndexView.as_view(),name='index'),
    path('api/v1/',include("api.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/',include('accounts.urls'))

]


admin.site.site_header = "Manga World Admin"
admin.site.site_title = "Manga World Admin Portal"
admin.site.index_title = "Welcome to Manga World Admin"
