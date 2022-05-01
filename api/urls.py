from django.urls import path,include
from . import views


appname="api"


urlpatterns = [
    path("search/",views.searchView,name='search'),
    path("user/",views.AccountsAPIView.as_view(),name='accounts'),
    path("manga/details/",views.MangaAPIView.as_view(),name='manga_details'),
    path("manga/popular/",views.get_popular_manga,name='popular')
]
