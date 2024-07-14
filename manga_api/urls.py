
from django.contrib import admin
from django.urls import path,include
from django.http.response import JsonResponse
from . import views
# from rest_framework.authtoken import views

def health_check(request):
    """health check"""
    return JsonResponse(data={'message': "up and running"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.IndexView.as_view(),name='index'),
    path('api/v1/',include("api.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/',include('accounts.urls')),
    path('health/check/', health_check)
]


admin.site.site_header = "Manga World Admin"
admin.site.site_title = "Manga World Admin Portal"
admin.site.index_title = "Welcome to Manga World Admin"
