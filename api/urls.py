from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from . import views as api_views

app_name = 'api'


schema_view = get_swagger_view(title='Tyne Music Api')


urlpatterns = [
    # docs/
    path('', schema_view, name='docs'),

    # /home-data/
    path('home-data/', api_views.HomeData.as_view(), name='home-data'),

    # categories/
    path('categories/', api_views.FetchCategories.as_view(), name='fetch-categories'),

    # albums/
    path('albums/', api_views.FetchAlbums.as_view(), name='fetch-albums'),

    # albums/invasion-of-privacy/
    path('albums/<slug:album_slug>/', api_views.FetchAlbum.as_view(), name='get-album'),

]
