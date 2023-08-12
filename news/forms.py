from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['categories', 'title', 'content', 'author']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['categories', 'title', 'content','author']