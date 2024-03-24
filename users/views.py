from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from .forms import ProfileForm
from django.views.decorators.csrf import csrf_protect

def register(request):
    if request.user.is_authenticated:
        return redirect('users:profile', pk=request.user.profile.id) 
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, f'The account {user.username} was created successfully, now you can login.')
            return redirect('users:edit_account')
        else:
            messages.error(request, 'Ooops something went wrong!')
    else:
        form = UserRegisterForm() 
    return render(request, 'register.html', {'form': form})

@csrf_protect
def login(request):
    if request.user.is_authenticated:
        return redirect('users:profile', pk=request.user.profile.id) 

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
            return redirect('users:profile', pk=request.user.profile.id)
        else:
            messages.error(request, 'Username OR Password is incorrect!')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form':form})


@login_required(login_url='users:login')
def edit_account(request):
    profile = request.user.profile
    print("profile",profile)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated!')
            return redirect('users:profile', pk=profile.id)
    context = {
        'form': form
    }
    return render(request, 'profile_form.html', context)

@login_required(login_url='users:login')
def delete_account(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'Account Deleted!')
        return redirect('weather:index')
    return render(request, 'delete_account.html')

@login_required 
def profile(request, pk):
    #user = User.objects.get(id=pk)
    profile = Profile.objects.get(id=pk)
    print("profile",profile)
    context = {
        'profile': profile
    }
    return render(request, 'profile.html', context)

@login_required 
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'User was successfully signed out!')
        return redirect('users:login')
    else:
        return render(request, 'logout.html')
