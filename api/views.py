from django.shortcuts import get_object_or_404
from rest_framework import views, generics

from music.models import Album, Artist, Genre, Category
from .serializers import AlbumSerializer, ArtistSerializer, GenreSerializer, CategorySerializer


class HomeData(views.APIView):

    @staticmethod
    def get(*args):
        albums = AlbumSerializer(
            instance=Album.objects.all(),
            many=True,
            read_only=True,
            no_songs=True
        ).data

        artists = ArtistSerializer(
            instance=Artist.objects.all(),
            many=True,
            read_only=True
        ).data

        genres = GenreSerializer(
            instance=Genre.objects.all(),
            many=True,
            read_only=True
        ).data

        return views.Response({
            'albums': albums,
            'artists': artists,
            'genres': genres
        })


class FetchCategories(views.APIView):
    """ get categories add 'for' as a query to get album or artist specific categories i.e. for=album or for=artist"""

    @staticmethod
    def get(request):
        categories = Category.objects.all()
        categories_for = request.GET.get('for', None)

        if categories_for == 'album':
            categories = categories.filter(album_category=True)
        elif categories_for == 'artist':
            categories = categories.filter(album_category=False)

        js_categories = CategorySerializer(categories, many=True, read_only=True).data

        return views.Response({
            'categories': js_categories
        })


class FetchAlbums(views.APIView):
    """ Fetch albums  """
    @staticmethod
    def get(request):
        """
        fetch published albums,
        add artist='name' in query to filter by artists

        for time period use
        1. before='YYYY-MM?-DD?' ->
        2. after='YYYY-MM?-DD?'
        3. on='YYYY-MM-DD'

        You can combine 1 and to get the above to

        """
        albums_data = AlbumSerializer(
            instance=Album.objects.filter(published=True),
            many=True,
            no_songs=True,
            read_only=True
        ).data
        return views.Response({
            'albums': albums_data
        })


class FetchAlbum(generics.RetrieveAPIView):
    queryset = Album.objects.filter(published=True)
    serializer_class = AlbumSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'album_slug'
