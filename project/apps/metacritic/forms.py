from django import forms
from django.conf import settings


class UrlForm(forms.Form):
    default_url = settings.PARSER_DEFAULT_PARSING_URL.format(
        platform=settings.PARSER_DEFAULT_PLATFORM
    )
    url = forms.URLField(
        label='url',
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': default_url,
                'size': '100'
            }
        ))
