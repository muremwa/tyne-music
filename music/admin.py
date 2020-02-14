from django.contrib import admin
from django.contrib import messages
from .models import Artist, Album, Genre, Song


class SongStackedInline(admin.StackedInline):
    model = Song
    extra = 3


@admin.register(Album)
class AlbumModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Info", {"fields": ["artist", "title", "description"]}),
        ("Details", {"fields": ["cover", "date_of_release"]}),
        ("ADD", {"fields": ["published"]}),
    ]
    list_display = ['title', 'artist', 'date_of_release', 'number_of_songs', 'published']
    list_filter = ['date_added', ]
    search_fields = ['title', 'artist', 'date_of_release']
    inlines = (SongStackedInline,)
    actions = ['publish_albums', 'un_publish_albums']

    @staticmethod
    def pluralize(upd):
        if upd == 1:
            return "1 album"
        else:
            return "{total} albums".format(total=upd)

    def publish_albums(self, request, queryset):
        updated = queryset.update(published=True)
        self.message_user(request, "{prefix} published".format(
            prefix=self.pluralize(updated),
        ))

    def un_publish_albums(self, request, queryset):
        updated = queryset.update(published=False)
        self.message_user(request, "{prefix} un published".format(
            prefix=self.pluralize(updated),
        ), level=messages.WARNING)


@admin.register(Song)
class SongModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Info", {"fields": ["track_number", "title", "album"]}),
        ("Details", {"fields": ["file", "year", "genres"]}),
    ]
    list_display = ['track_number', "title", "length", "album"]
    list_filter = ['album', ]
    search_fields = ['title', 'album', 'genres']


admin.site.register(Artist)
admin.site.register(Genre)
