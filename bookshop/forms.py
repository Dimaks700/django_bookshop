from dataclasses import fields
from django import forms

from bookshop.models import Comment

class SearchForm(forms.Form):
    name = forms.CharField(label='Введите название книги:')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
