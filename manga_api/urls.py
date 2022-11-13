
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.IndexView.as_view(),name='index'),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/',include('accounts.urls')),
    path('api/v1/',include("api.urls")),
]


admin.site.site_header = "Manga World Admin"
admin.site.site_title = "Manga World Admin Portal"
admin.site.index_title = "Welcome to Manga World Admin"
