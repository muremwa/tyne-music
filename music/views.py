from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from django.http import Http404

from .models import Album, Artist, Genre


class MusicIndex(View):
    def get(self, *args, **kwargs):
        # fetch some albums
        albums = Album.objects.filter(published=True).order_by('-date_added')

        # fetch some genres
        genres = Genre.objects.all()

        # fetch some artists
        artists = set()
        for album in albums:
            artists.add(album.artist)

        return render(self.request, 'music/index.html', {
            'albums': albums,
            'genres': genres,
            'artists': sorted(list(artists), key=lambda artist: artist.total_songs(), reverse=True),
        })


class AlbumPage(generic.DetailView):
    model = Album
    context_object_name = 'album'
    slug_url_kwarg = 'slug'
    template_name = 'music/album.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # make sure the album is published
        album = context.get('album', None)
        if not album.published:
            raise Http404

        return context


class ArtistPage(generic.DetailView):
    model = Artist
    context_object_name = 'artist'
    slug_url_kwarg = 'slug'
    template_name = 'music/artist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # albums by this artist
        artist = context.get('artist', None)
        context['albums'] = artist.album_set.filter(published=True)
        return context


class GenrePage(View):
    def get(self, *args, **kwargs):
        # retrieve being queried from the url
        genre = get_object_or_404(
            Genre,
            slug=kwargs.get('genre_name', None)
        )

        # fetch some songs in the genre
        songs = genre.song_set.filter(
            album__published=True
        )[:20]   # limit to 20

        # render the page
        return render(self.request, 'music/genre.html', {
            'genre': genre,
            'songs': songs,
        })
