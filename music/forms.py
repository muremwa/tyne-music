from django.forms import ModelForm, HiddenInput
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as __

from .models import Category


class CategoryFormClean(ModelForm):
    def clean(self):
        data = self.cleaned_data

        # ensure if an item has album_category as True then that no artist_items are there and vice versa
        if 'album_items' in data and 'artist_items' in data:
            if data.get('album_category') and data.get('artist_items').count() > 0:
                raise ValidationError(__('An album category cannot include artists'), code='true-category')

            if not data.get('album_category') and data.get('album_items').count() > 0:
                raise ValidationError(__('An artist category cannot include albums'), code='false-category')

        return data


class CategoryModelForm(CategoryFormClean):
    class Meta:
        model = Category
        fields = '__all__'

    class Media:
        js = ('cu_admin/js/categorySwitch.js',)


class AlbumCategoryModelForm(CategoryFormClean):
    class Meta:
        model = Category
        exclude = ('artist_items',)
        widgets = {
            'album_category': HiddenInput()
        }


class ArtistCategoryModelForm(CategoryFormClean):
    class Meta:
        model = Category
        exclude = ('album_items',)
        widgets = {
            'album_category': HiddenInput()
        }
