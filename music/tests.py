from django.test import TestCase
from music.models import Artist, Album, Genre, Song
from django.core.files import File
from django.utils.text import slugify

from mock import MagicMock
from datetime import datetime


class ModelsTestCase(TestCase):
    def setUp(self):
        # artist
        self.artist = Artist(
            name='Baby Kaely',
            date_of_birth=datetime(2004, 11, 26),
            country='United states of America',
        )
        self.artist.save()

        # album
        self.album = Album(
            title='The Hangout',
            artist=self.artist,
            description="tyne test",
            date_of_release=datetime(2019, 10, 10),
        )
        self.album.save()

        # genre
        self.genre = Genre(
            name='R&B',
        )
        self.genre.save()

        # song
        self.song_mock = MagicMock(spec=File)   # mock the music file
        self.song_mock.name = 'blue.mp3'

        self.song = Song(
            track_number=1,
            title='hangout',
            album=self.album,
            year=datetime(2019, 10, 10),
            file=self.song_mock,
        )
        self.song.save()

    def test_instance_slugs(self):
        self.assertEqual(self.artist.slug, slugify(self.artist.name) + "-" + str(self.artist.pk))
        self.assertEqual(self.album.slug, slugify(self.album.title))
        self.assertEqual(self.genre.slug, slugify(self.genre.name))

    def test_absolute_url(self):
        self.assertEqual(self.artist.get_absolute_url(), '/music/artist/{slug}/'.format(slug=self.artist.slug))
        self.assertEqual(self.album.get_absolute_url(), '/music/album/{slug}/'.format(slug=self.album.slug))
        self.assertEqual(self.genre.get_absolute_url(), '/music/genre/{slug}/'.format(slug=self.genre.slug))
        self.assertEqual(
            self.song.get_absolute_url(),
            '/music/album/{album_slug}/#track-{track_number}'.format(
                album_slug=self.song.album.slug,
                track_number=self.song.track_number,
            )
        )
