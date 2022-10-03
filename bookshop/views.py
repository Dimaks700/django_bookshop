from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from requests import request
from .forms import CommentForm
from django.db.models import Sum

from .models import Book, Author, Comment, Cart, User
import bookshop.forms

class HomeListView(generic.ListView):
    model = Book
    paginate_by = 10
    template_name = 'bookshop/home.html'
    ordering = ['id']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['cart_items'] = Cart.objects.get(cart_man = self.request.user).cart_items.count()
            except Cart.DoesNotExist:
                return context
        return context

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'bookshop/detail.html'
    context_object_name = 'book'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_book = Book.objects.get(pk=self.kwargs.get('pk'))
        comment_list = current_book.comments.all()
        total_likes = [i.total_likes() for i in comment_list]
        context['total_likes'] = total_likes
        return context

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
        name = Book.objects.filter(book_name__icontains=search) 
        #В SQLite поиск всяких символов кроме ASCII case-sensitive, icontains не работает
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
        name = f"{self.request.user.first_name} {self.request.user.last_name}"
        form.instance.author = name
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.kwargs['pk']})

def cart(request):
    if request.method == 'POST':
        if request.POST.get('delete_book') == 'delete_book':
            book_pk = request.POST.get('book_pk')
            man = Cart.objects.get(cart_man = request.user)
            book_delete = man.cart_items.remove(book_pk)
            
        elif request.POST.get('clear_cart') == "clear_cart":
            Cart.objects.filter(cart_man__exact=request.user.id).delete()
            return render(request, 'bookshop/cart.html')
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
            return render(request, 'bookshop/cart.html')

    man = Cart.objects.get(cart_man = request.user)
    items = man.cart_items.all()
    total_sum = items.aggregate(Sum('price'))['price__sum']
    context = {'user_name': man, 'new_book': items, 'total_sum': total_sum}

    return render(request, 'bookshop/cart.html', context)

def LikeView(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id')) 
    liked = False
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('book_detail', args=[str(pk)]))
