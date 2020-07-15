from django.forms import ModelForm

from .models import Category


class CategoryModelForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    class Media:
        js = ('cu_admin/js/categorySwitch.js',)


class AlbumCategoryModelForm(ModelForm):
    class Meta:
        model = Category
        exclude = ('artist_items', 'album_category')


class ArtistCategoryModelForm(ModelForm):
    class Meta:
        model = Category
        exclude = ('album_items', 'album_category')
