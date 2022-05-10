from dataclasses import fields
from django import forms

from bookshop.models import Author, Book, Jenre, Language, Comment

class SearchForm(forms.Form):
    name = forms.CharField(label='Введите название книги:')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'body')