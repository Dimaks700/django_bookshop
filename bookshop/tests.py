from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
import bookshop.views as views

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, views.HomeListView)
    
    def test_author_url_is_resolved(self):
        url = reverse('about_me')
        self.assertEquals(resolve(url).func.view_class, views.AboutAuthorPage)
        
    def test_search_url_is_resolved(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, views.search)
    
    def test_cart_url_is_resolved(self):
        url = reverse('cart')
        self.assertEquals(resolve(url).func, views.cart)

    def test_purchase_url_is_resolved(self):
        url = reverse('purchase')
        self.assertEquals(resolve(url).func, views.cart_purchase)
        
    def test_book_detail_url_is_resolved(self):
        url = reverse('book_detail', args=["1"])
        self.assertEquals(resolve(url).func.view_class, views.BookDetailView)
        url_2 = reverse('book_detail', args=["20"])
        self.assertEquals(resolve(url_2).func.view_class, views.BookDetailView)

class TestViews(TestCase):
    
    def test_home_GET(self):
        client = Client() 
        response = client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookshop/home.html')
        
    def test_author_GET(self):
        client = Client() 
        response = client.get(reverse('about_me'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookshop/about_me.html')
                
    def test_cart_GET(self):
        client = Client() 
        response = client.get(reverse('cart'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookshop/cart.html')
