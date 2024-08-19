from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from favourites.api import fetch_anime_statistics
import requests
from favourites.models import Favourite
from django.core.cache import cache
from django.contrib import messages

BASE_URL = "https://api.jikan.moe/v4/"

BASE_URL_ANIME = 'https://api.jikan.moe/v4/anime/'

BASE_URL_CHARACTER = 'https://api.jikan.moe/v4/characters/'


def anime_statistics(request, anime_id):
    cache_key = f"anime_{anime_id}_statistics"
    data = cache.get(cache_key)
    if not data:
        try:
            data = fetch_anime_statistics(anime_id)
            cache.set(cache_key, data, timeout=60*15)  # Cache for 15 minutes
        except requests.HTTPError as e:
            data = {"error": str(e)}
    return render(request, 'anime_statistics.html', {'data': data['data']})


# @login_required
# def add_to_favourites_anime(request, anime_id):
#     Favourite.objects.get_or_create(user=request.user, anime_id=anime_id)
#     return redirect('anime:details', anime_id=anime_id)


# for favourites in anime_details
@login_required
def add_to_favourites_anime(request, anime_id):
    if not Favourite.objects.filter(user=request.user, anime_id=anime_id).exists():
        Favourite.objects.create(user=request.user, anime_id=anime_id)
        messages.success(request, 'Successfully added to favourites')
    return redirect('anime:details', anime_id=anime_id)


@login_required
def add_to_favourites_character(request, character_id):
    Favourite.objects.get_or_create(user=request.user, character_id=character_id)
    return redirect('anime:character_details', character_id=character_id)


@login_required
def favourites(request):
    favourite_items = Favourite.objects.filter(user=request.user)
    animes = []
    characters = []
    for item in favourite_items:
        if item.anime_id:
            response = requests.get(f"{BASE_URL_ANIME}{item.anime_id}")
            if response.status_code == 200:
                animes.append(response.json()['data'])
        elif item.character_id:
            response = requests.get(f"{BASE_URL_CHARACTER}{item.character_id}")
            if response.status_code == 200:
                characters.append(response.json()['data'])
    return render(request, 'favourites.html', {'animes': animes, 'characters': characters})


@login_required
def remove_from_favourites(request, anime_id):
    Favourite.objects.filter(user=request.user, anime_id=anime_id).delete()
    return redirect('favourites:favourites')


@login_required
def empty_favourites(request):
    Favourite.objects.filter(user=request.user).delete()
    return redirect('favourites:favourites')