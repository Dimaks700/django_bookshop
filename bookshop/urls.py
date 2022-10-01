from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.HomeListView.as_view(), name='home'),
    path('<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('author/<pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('add_book', views.CreateBookView.as_view(), name='add_book'),
    path('<pk>/update_book/', views.BookUpdateView.as_view(), name='update_book'),
    path('<pk>/delete_book/', views.DeleteBookView.as_view(), name='delete_book'),
    path('creator/', views.AboutAuthorPage.as_view(), name='about_me'),
    path('<pk>/update_author', views.AuthorUpdateView.as_view(), name='update_author'),
    path('search', views.search, name='search'), 
    path('add_author/', views.CreateAuthorView.as_view(), name='create_author'),
    path('<int:pk>/add_comment/', views.CommentCreateView.as_view(), name='create_comment'),
    path('cart', views.cart, name='cart')
]