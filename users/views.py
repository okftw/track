# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.
def index(request):
    return render(request, 'users/signup.html' )

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('tracker:index')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
               return redirect('tracker:index')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', { 'form': form })

def logout_view(request):
    if request.method == 'GET':
            logout(request)
            return redirect('tracker:index')
    else:
        return "YOU ARE LOGGED OUT"
