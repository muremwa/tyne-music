from django.shortcuts import get_object_or_404
from rest_framework import views

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
    """ Fetch albums or an album. To fetch a single album, pass album-slug='slug' into the query """
    @staticmethod
    def get(request):
        data = {}
        album_slug = request.GET.get('album-slug', None)

        if album_slug:
            album = get_object_or_404(Album, slug=album_slug)
            data['album'] = AlbumSerializer(instance=album, read_only=True).data

        else:
            albums = Album.objects.all()
            data['albums'] = AlbumSerializer(instance=albums, many=True, read_only=True, no_songs=True).data

        return views.Response(data)
