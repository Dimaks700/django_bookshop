from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from .forms import CommentForm
from django.db.models import Sum

from .models import Book, Author, Comment, Cart, User
import bookshop.forms

class HomeListView(generic.ListView):
    model = Book
    paginate_by = 10
    template_name = 'bookshop/home.html'
    ordering = ['id']
    
class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'bookshop/detail.html'
    context_object_name = 'book'

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'bookshop/about_author.html'
    context_object_name = 'author'

class CreateBookView(CreateView):
    model = Book
    template_name = 'bookshop/create_book.html'
    fields = ['book_name', 'description', 'pages', 'price', 'language', 'author', 'genre', 'photo']

class BookUpdateView(UpdateView):
    model = Book 
    fields = ['book_name', 'description', 'pages', 'price', 'language', 'author', 'genre', 'photo']
    template_name = 'bookshop/update_book.html'

class DeleteBookView(DeleteView):
    model = Book  
    fields = ['book_name', 'description', 'pages', 'price', 'language', 'author', 'genre']
    success_url = reverse_lazy('home')

class AboutAuthorPage(TemplateView):
    template_name = 'bookshop/about_me.html'
    
class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['author_name', 'author_description']
    template_name = 'bookshop/update_author.html'

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        name = Book.objects.filter(book_name__contains=search)
        number = name.count()
        return render(request, 'bookshop/search_result.html', 
        {'search':search, 'name':name, 'number': number})
    else:
        return render(request, 'bookshop/search_result.html')

class CreateAuthorView(CreateView):
    model = Author
    template_name = 'bookshop/create_author.html'
    fields = ['author_name', 'author_description']

class CommentCreateView(CreateView):
    model = Comment
    template_name = 'bookshop/add_comment.html'
    form_class = CommentForm
    def form_valid(self, form):
        form.instance.book_id = self.kwargs['pk']
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.kwargs['pk']})

def user_profile(request, user_name):
    if request.method == 'POST':
        if request.POST.get('delete_book') == 'delete_book':
            book_pk = request.POST.get('book_pk')
            man = Cart.objects.get(cart_man = request.user)
            book_delete = man.cart_items.remove(book_pk)
            #return HttpResponse('ok')
            
        elif request.POST.get('clear_cart') == "clear_cart":
            Cart.objects.filter(cart_man__exact=request.user.id).delete()
            return render(request, 'bookshop/profile.html')
        else:
            new_book_pk = request.POST.get('book_pk')
            new_book = Book.objects.get(pk=new_book_pk)
            if Cart.objects.filter(cart_man__exact=request.user.id).exists():
                man = Cart.objects.get(cart_man = request.user)
                man.cart_items.add(new_book)
            else:
                c = Cart(cart_man = request.user)
                c.save()
                c.cart_items.add(new_book)
    else:
        if not Cart.objects.filter(cart_man__exact=request.user.id).exists():
            return render(request, 'bookshop/profile.html')

    man = Cart.objects.get(cart_man = request.user)
    items = man.cart_items.all()
    total_sum = items.aggregate(Sum('price'))['price__sum']
    context = {'user_name': man, 'new_book': items, 'total_sum': total_sum}

    return render(request, 'bookshop/profile.html', context)
