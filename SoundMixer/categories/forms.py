from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

from django import forms
from .models import Category

def validate_tag(value):
    # determines if a fraction name is a real fraction
    # or a bunch of gibberish
    try:
        Category.objects.get(name = value)
    except:
        raise ValidationError(
            gettext_lazy('/f/%(value)s is not a valid tag'),
            params={'value': value},
        )

class TagField(forms.CharField):
    def to_python(self, value):
        # Normalizes the data to a list of strings.
        # Return an empty list if no input was given.
        if not value:
            return []
        t_list = value.split(',')
        # eliminates any whitespace on the begining or end of a fraction name.
        t_list = [x.strip() for x in t_list]
        return t_list

    def validate(self, value):
        # Check if list contains only real fractions
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for tag in value:
            validate_tag(tag)

class LinkField(forms.CharField):
    def to_python(self, value):
        components = value.split('?v=')
        info = components[-1].split('&')
        return info[0]

class SongForm(forms.Form):
    #used to make a new post in the text_post view
    name = forms.CharField(label = 'Post Title', max_length = 280)
    link = LinkField(label = 'Post link', max_length = 50)
    tags = TagField(label = 'List tags seperated by a comma', max_length = 1000)

class SearchForm(forms.Form):
    include = TagField(label = 'Must include:', max_length = 1000, required=False)
    exclude = TagField(label = 'Can\'t have', max_length = 1000, required=False)
