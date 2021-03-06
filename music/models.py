from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Artist(models.Model):
    name = models.CharField(max_length=100, help_text="Enter their stage name")
    date_of_birth = models.DateField()
    country = models.CharField(max_length=100, help_text="Enter home country")
    slug = models.SlugField(blank=True, null=True)
    avi = models.ImageField(
        upload_to='artists/',
        default='defaults/artist.png',
        null=True,
        blank=True,
        help_text="Preferably 4:3"
    )
    objects = models.Manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # save first in order to get the pk
        super().save(args, kwargs)

        # add the pk to the slug url
        self.slug = slugify(str(self.name) + "-" + str(self.pk))
        super().save()

    @property
    def dob(self):
        return self.date_of_birth.strftime('%B %d, %Y')

    def total_songs(self):
        return sum(
            [album.number_of_songs for album in list(self.album_set.all())]
        )

    def get_absolute_url(self):
        return reverse('music:artist', kwargs={
            'slug': self.slug,
        })

    def get_absolute_api_url(self):
        return reverse("api:get-artist", kwargs={"artist_slug": str(self.slug)})


class Album(models.Model):
    title = models.CharField(max_length=100, unique=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    description = models.TextField(help_text="Some details behind the conception of the album")
    date_of_release = models.DateField()
    date_added = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False, help_text="This should be marked true if the album is ready")
    slug = models.SlugField(blank=True, unique=True)
    cover = models.ImageField(
        upload_to='album_covers/',
        default='defaults/album_cover.png',
        null=True,
        blank=True,
        help_text="Preferably 4:3"
    )
    objects = models.Manager()

    def __str__(self):
        return "{album}({year})".format(album=self.title, year=self.date_of_release.year)

    def save(self, *args, **kwargs):
        # slug url
        self.slug = slugify(str(self.title))
        return super().save(args, kwargs)

    def get_absolute_url(self):
        return reverse('music:album', kwargs={
            'slug': self.slug,
        })
    
    def get_absolute_api_url(self):
        return reverse("api:get-album", kwargs={"album_slug": str(self.slug)})
    
    @property
    def songs_url(self):
        return reverse("api:fetch-album-songs", kwargs={"album_slug": str(self.slug)})

    @property
    def year(self):
        return self.date_of_release.strftime('%Y')

    def get_clean_release_date(self):
        return self.date_of_release.strftime("%B %d, %Y")

    def play_now(self):
        return self.song_set.order_by('track_number')[0].play_now()
        
    @property
    def number_of_songs(self):
        return self.song_set.count()


class Genre(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='genres/', default='defaults/genre.png', null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # slug url
        self.slug = slugify(str(self.name))
        return super().save(args, kwargs)

    def get_absolute_url(self):
        return reverse('music:genre', kwargs={
            'genre_name': self.slug,
        })

    def get_absolute_api_url(self):
        return reverse("api:get-genre", kwargs={"genre_slug": str(self.slug)})


def upload_music_to(instance, filename):
    return "music/{album_name}/{file_name}".format(
        file_name=filename,
        album_name=instance.album,
    )


class Song(models.Model):
    track_number = models.IntegerField(help_text="Should be unique for every song in the album")
    title = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    year = models.DateField()
    genres = models.ManyToManyField(Genre, verbose_name='Song\'s genres')
    file = models.FileField(upload_to=upload_music_to)
    length = models.CharField(help_text="in the form of 3:40", max_length=10, default="0:00")
    objects = models.Manager()

    def __str__(self):
        return "{title} from {album} by {artist}".format(
            album=self.album.title,
            artist=self.album.artist.name,
            title=self.title
        )

    def get_absolute_url(self):
        return "{album_url}#track-{pk}-{track_number}".format(
            track_number=self.track_number,
            album_url=self.album.get_absolute_url(),
            pk=self.pk
        )

    def play_now(self):
        return self.get_absolute_url() + "&play=true"

    @property
    def artist(self):
        return self.album.artist

    @property
    def genre(self):
        return self.genres.all()[0]


class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    album_category = models.BooleanField(default=True)
    avi = models.ImageField(upload_to='categories/', default='defaults/category.png', null=True, blank=True)
    album_items = models.ManyToManyField(Album, blank=True)
    artist_items = models.ManyToManyField(Artist, blank=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Categories"

    @property
    def items(self):
        category_items = self.album_items
        if not self.album_category:
            category_items = self.artist_items
        return category_items

    def __str__(self):
        return f"Category titled {self.title}"
