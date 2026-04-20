from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Post


class MultipleFileInput(ClearableFileInput):
    """A file input that accepts multiple files."""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """FileField that handles multiple uploaded files."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class PostForm(forms.ModelForm):
    images = MultipleFileField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'description', 'post_type', 'city', 'price']


class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        max_length=500,
    )
