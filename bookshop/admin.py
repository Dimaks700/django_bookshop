from django.contrib import admin
from .models import Book, Cart, Jenre, Author, Language, Comment
# Register your models here.

admin.site.register(Book)
admin.site.register(Jenre)
admin.site.register(Author)
admin.site.register(Language)
admin.site.register(Comment)
admin.site.register(Cart)
