from django.contrib.auth import login as dj_login, authenticate, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render

from mainMessages.models import UserProfile
from registration.forms import SignupForm, LoginForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            dj_login(request, user)

            UserProfile.objects.create(
                user=User.objects.get(username=user),
                nickname=user,
            )

            return redirect('/')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')

        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                dj_login(request, user)
                return redirect('/')

    return render(request, 'login.html', {'form': form})


def logout(request):
    dj_logout(request)
    return redirect('/')


@login_required
def profile(request):
    if request.method == 'GET':
        if request.user.is_authenticated is not True:
            return redirect('/login')
        user = UserProfile.objects.get(user=request.user)
        return render(request, 'profile.html', {'p_user': user})
    else:
        p_user = UserProfile.objects.get(user=request.user)

        if 'avatar' in request.FILES:
            file = request.FILES['avatar']
            p_user.avatar = file

        nickname = request.POST['nickname']
        p_user.nickname = nickname

        p_user.save()

        return redirect('/profile')
