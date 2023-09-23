from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=3)

    class Meta:
        model = Post
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if text == title:
            raise ValidationError('Заголовок и текст должны отличаться!')

        return cleaned_data
