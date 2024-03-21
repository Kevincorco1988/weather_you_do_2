from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.user.is_authenticated:
        return redirect('weather:index')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, f'The account {user.username} was created successfully, now you can login.')
            return redirect('users:login')
        else:
            messages.error(request, 'Ooops something went wrong!')
    else:
        form = UserRegisterForm() 
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('weather:index')

    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except Exception:
            messages.error(request, 'Username does not exist!')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('weather:index')
        else:
            messages.error(request, 'Username OR Password is incorrect!')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form':form})


@login_required 
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'User was successfully signed out!')
        return redirect('users:login')
    else:
        return render(request, 'logout.html')
