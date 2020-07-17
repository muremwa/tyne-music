from rest_framework.serializers import ModelSerializer

from music.models import Album, Genre, Song, Artist, Category


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class SongSerializer(ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Song
        fields = '__all__'


class AlbumSerializer(ModelSerializer):
    songs = SongSerializer(source='song_set', many=True)

    def __init__(self, *args, **kwargs):
        no_songs = kwargs.pop('no_songs', False)

        super(AlbumSerializer, self).__init__(*args, **kwargs)

        if no_songs:
            self.fields.pop('songs')

    class Meta:
        model = Album
        fields = '__all__'


class ArtistSerializer(ModelSerializer):
    albums = AlbumSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    artist_items = ArtistSerializer(many=True, read_only=True)
    album_items = AlbumSerializer(many=True, read_only=True, no_songs=True)

    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.album_category:
            data['items'] = data.pop('album_items')
            data.pop('artist_items')
        else:
            data['items'] = data.pop('artist_items')
            data.pop('album_items')

        return data
