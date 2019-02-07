from django import forms
from django.conf import settings


class UrlForm(forms.Form):
    url = forms.URLField(
        label='url',
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': settings.DEFAULT_PARSING_URL.format(platform=settings.DEFAULT_PLATFORM),
                'size': '100'
            }
        ))
