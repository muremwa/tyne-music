import datetime
import re

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
    """
    fetch published albums,
    add artist='name' in query to filter by artists

    for time period use
    1. before='YYYY-MM-DD' -> before a certain date
    2. after='YYYY-MM-DD' -> after a certain date
    3. on='YYYY-MM-DD' -> on a certain date

    You can combine 1 and 2 to filter albums between two dates
    ?after='YYYY-MM-DD'&'before='YYYY-MM-DD'
        the dates should not conflict e.g. before 2017 but after 2019

    """

    @staticmethod
    def is_time_format_valid(current_date: str) -> bool:
        valid = False

        if re.search('\d{4}-\d{2}-\d{2}', current_date):
            date = [int(char) for char in current_date.split('-')]

            if len(date) == 3:
                try:
                    datetime.datetime(date[0], date[1], date[2])
                    valid = True
                except ValueError:
                    pass

        return valid

    def time_filter(self, q_set, params):
        """ date_of_release time filters """

        for key, item in params.items():
            if self.is_time_format_valid(item):
                if key == 'before':
                    q_set = q_set.filter(date_of_release__lte=item)

                elif key == 'after':
                    q_set = q_set.filter(date_of_release__gte=item)

                elif key == 'on':
                    q_set = q_set.filter(date_of_release=item)

        return q_set

    def get(self, request):
        albums = Album.objects.filter(published=True)

        # filter by artist
        artist = request.GET.get('artist', None)
        if artist:
            albums = albums.filter(artist__name__icontains=artist)

        # time filters
        time_filters = {
            'before': request.GET.get('before', ''),
            'after': request.GET.get('after', ''),
            'on': request.GET.get('on', ''),
        }

        if any(time_filters.values()):
            albums = self.time_filter(albums, time_filters)

        albums_data = AlbumSerializer(
            instance=albums,
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
