from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    author_name = models.CharField(max_length=80) 
    author_description = models.TextField()
    def __str__(self) -> str:
        return self.author_name
    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'pk':self.pk})

class Jenre(models.Model):
    jenre_type = models.CharField(max_length=80)
    def __str__(self) -> str:
        return self.jenre_type

class Language(models.Model):
    book_language = models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.book_language

class Book(models.Model):
    book_name = models.CharField(max_length=90, verbose_name="Название книги")
    description = models.TextField(verbose_name="Описание")
    pages = models.IntegerField(verbose_name="Количество страниц")
    price = models.IntegerField(verbose_name="Цена")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="Язык")
    author = models.ManyToManyField(Author, verbose_name="Автор")
    genre = models.ManyToManyField(Jenre, verbose_name="Жанр")
    photo = models.ImageField(null=True, blank=True, upload_to="images/")
    
    def __str__(self):
        return self.book_name

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk':self.pk})
    
class Comment(models.Model):
    author = models.CharField(max_length=255)
    body = models.TextField()
    book = models.ForeignKey(Book, related_name="comments", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='user_likes')
    
    def __str__(self):
        return self.author

    def total_likes(self): 
        return self.likes.count()

class Cart(models.Model):
    cart_man = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(Book)
    def __str__(self) -> str:
        return self.cart_man.first_name
