from rest_framework.views import APIView, Response

from music.models import Album, Artist, Genre, Category
from .serializers import AlbumSerializer, ArtistSerializer, GenreSerializer, CategorySerializer


class HomeData(APIView):

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

        return Response({
            'albums': albums,
            'artists': artists,
            'genres': genres
        })


class FetchCategories(APIView):

    @staticmethod
    def get(request):
        categories = Category.objects.all()
        categories_for = request.GET.get('for', None)

        if categories_for == 'album':
            categories = categories.filter(album_category=True)
        elif categories_for == 'artist':
            categories = categories.filter(album_category=False)

        js_categories = CategorySerializer(categories, many=True, read_only=True).data

        print(js_categories)

        return Response({
            'categories': js_categories
        })
