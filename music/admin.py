from django.contrib import admin
from .models import Artist, Album, Genre, Song


class SongStackedInline(admin.StackedInline):
    model = Song
    extra = 5


@admin.register(Album)
class AlbumModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Info", {"fields": ["artist", "title", "description"]}),
        ("Details", {"fields": ["cover", "date_of_release"]}),
        ("ADD", {"fields": ["published"]}),
    ]
    list_display = ['title', 'artist', 'date_of_release', 'published']
    list_filter = ['date_added', ]
    search_fields = ['title', 'artist', 'date_of_release']
    inlines = (SongStackedInline,)


@admin.register(Song)
class SongModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Info", {"fields": ["track_number", "title", "album"]}),
        ("Details", {"fields": ["file", "year", "genres"]}),
    ]
    list_display = ['track_number', "title", "album"]
    list_filter = ['album', ]
    search_fields = ['title', 'album', 'genres']


admin.site.register(Artist)
admin.site.register(Genre)
