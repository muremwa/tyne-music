from rest_framework import serializers

from music.models import Album, Genre, Song, Artist, Category


class GenreSerializer(serializers.ModelSerializer):
    genre = serializers.CharField(source='name')
    genre_slug = serializers.CharField(source='slug')
    cover = serializers.ImageField(source='image')

    class Meta:
        model = Genre
        exclude = ('id', 'name', 'image', 'slug')


class SongSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, required=False)

    class Meta:
        model = Song
        exclude = ('genres', 'id', 'year', 'album',)


class AlbumSerializer(serializers.ModelSerializer):
    songs = SongSerializer(source='song_set', many=True)
    year = serializers.CharField()
    artist = serializers.CharField(source='artist.name')
    artist_slug = serializers.SlugField(source='artist.slug')
    album_cover = serializers.ImageField(source='cover')
    album_slug = serializers.SlugField(source='slug')

    def __init__(self, *args, **kwargs):
        no_songs = kwargs.pop('no_songs', False)

        super(AlbumSerializer, self).__init__(*args, **kwargs)

        if no_songs:
            self.fields['songs'] = serializers.URLField(source='songs_url')

    class Meta:
        model = Album
        exclude = ('date_of_release', 'date_added', 'published', 'id', 'cover', 'slug')


class ArtistSerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True, required=False, read_only=True)
    artist_slug = serializers.CharField(source='slug')
    dob = serializers.CharField()

    class Meta:
        model = Artist
        exclude = ('date_of_birth', 'id', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source='title')
    category_description = serializers.CharField(source='description')
    category_avi = serializers.ImageField(source='avi')
    artist_items = ArtistSerializer(many=True, read_only=True)
    album_items = AlbumSerializer(many=True, read_only=True, no_songs=True)

    class Meta:
        model = Category
        exclude = ('id', 'title', 'description', 'avi',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.album_category:
            data['items'] = data.pop('album_items')
            data.pop('artist_items')
        else:
            data['items'] = data.pop('artist_items')
            data.pop('album_items')

        return data
