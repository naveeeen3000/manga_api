
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from rest_framework import routers, serializers, viewsets
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.MangaWorldAPI.as_view(),name='index'),
    path('api/v1/',include("api.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/',include('accounts.urls')),
    path('favicon',RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))
]


admin.site.site_header = "Manga World Admin"
admin.site.site_title = "Manga World Admin Portal"
admin.site.index_title = "Welcome to Manga World Admin"
