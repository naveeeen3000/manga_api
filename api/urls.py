from django.urls import path,include
from . import views


appname="api"


urlpatterns = [
    path("search/",views.searchView,name='search'),
    path("user/",views.AccountsAPIView.as_view(),name='accounts'),
    path("manga/details/",views.MangaAPIView.as_view(),name='manga_details'),
    path("manga/popular/",views.get_popular_manga,name='popular'),
    path("manga/",views.get_manga_by_genre,name='genre'),
    path("manga/tags/",views.get_anime_by_tags,name='tags'),
    path('manga/read/',views.get_read_manga,name='read_manga')
]
