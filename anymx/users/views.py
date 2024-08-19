from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreate, UserChange
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import requests
from favourites.models import Favourite
from watchlist.models import Watchlist

BASE_URL = "https://api.jikan.moe/v4/"

BASE_URL_ANIME = 'https://api.jikan.moe/v4/anime/'

BASE_URL_CHARACTER = 'https://api.jikan.moe/v4/characters/'


def register(request):
    if request.method == 'POST':
        form = UserCreate(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('anime:all_page')
    else:
        form = UserCreate()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('anime:all_page')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
# form.cleaned_data: After the form is validated (form.is_valid()), Django's form system automatically performs
# validation checks based on the rules defined in the form class (AuthenticationForm in this case).
# This cleaned_data attribute is a dictionary that contains the validated user input from the form fields.

# The AuthenticationForm() instance handles form creation and validation in Django.

# @login_required()
# def profile(request):
#     user = request.user # calls the current user
#     p_data = {
#         'avatar': user.avatar.url if user.avatar else None,
#         'username': user.username,
#         'email': user.email
#     }
#     return render(request,'profile.html',p_data)

@login_required()
def profile(request):
    user = request.user
    watchlist_items = Watchlist.objects.filter(user=user)
    favourite_items = Favourite.objects.filter(user=user)
    animes = []
    characters = []
    for item in watchlist_items:
        response = requests.get(f"{BASE_URL}{item.anime_id}")
        if response.status_code == 200:
            animes.append(response.json()['data'])
    for item in favourite_items:
        if item.anime_id:
            response = requests.get(f"{BASE_URL_ANIME}{item.anime_id}")
            if response.status_code == 200:
                animes.append(response.json()['data'])
        elif item.character_id:
            response = requests.get(f"{BASE_URL_CHARACTER}{item.character_id}")
            if response.status_code == 200:
                characters.append(response.json()['data'])
    context = {
        'avatar': user.avatar.url if user.avatar else None,
        'username': user.username,
        'email': user.email,
        'watchlist_items': animes,
        'favourite_items': animes + characters,
    }
    return render(request, 'profile.html', context)


@login_required()
def profile_update(request):
    if request.method == 'POST':  # if request is POST i.e, the user submitted the form
        form = UserChange(request.POST, request.FILES, instance=request.user) # instance=request.user bind it to the current user (instance=request.user).
        if form.is_valid():
            form.save()
            return redirect('users:profile')  # Redirect to profile page
    else:
        form = UserChange(instance=request.user)
        # GET Method: If the request method is GET, it means the user is accessing the page to view the form.
        # form = UserChange(instance=request.user): Initializes the UserChange form with the current user's data
        # (instance=request.user). This pre-populates the form fields with the user's existing information.

    return render(request, 'profile_update.html', {'form': form})


@login_required()
def logout_user(request):
    logout(request)
    return login_user(request)

