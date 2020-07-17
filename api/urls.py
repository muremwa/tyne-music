from django.urls import path

from . import views as api_views

app_name = 'api'


urlpatterns = [
    # /home-data/
    path('home-data/', api_views.HomeData.as_view(), name='home-data'),

    # categories/
    path('categories/', api_views.FetchCategories.as_view(), name='fetch-categories'),

    # albums/
    path('albums/', api_views.FetchAlbums.as_view(), name='fetch-albums'),

]
