from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CreationFrom 
# Create your views here.

class SignUp(CreateView):
    form_class = CreationFrom
    success_url = reverse_lazy('home')
    template_name = 'users/signup.html' 
