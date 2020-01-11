from django.urls import path

from . import views


app_name = "music"


urlpatterns = [

    # music/
    path('', views.MusicIndex.as_view(), name="index"),

    # music/album/divide/
    path('album/<slug:slug>/', views.AlbumPage.as_view(), name="album"),

    # /music/artist/ed-sheraan-1/
    path('artist/<slug:slug>/', views.ArtistPage.as_view(), name="artist"),

    # /music/genre/r&b/
    path('genre/<genre_name>/', views.GenrePage.as_view(), name="genre"),

]
