from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from watchlist.models import Watchlist
import requests
from django.contrib import messages

BASE_URL = 'https://api.jikan.moe/v4/anime/'

# @login_required
# def add_to_watchlist(request, anime_id):
#     Watchlist.objects.get_or_create(user=request.user, anime_id=anime_id)
#     return redirect('anime:details', anime_id=anime_id)


# for watchlist in anime_details
@login_required
def add_to_watchlist(request, anime_id):
    if not Watchlist.objects.filter(user=request.user, anime_id=anime_id).exists():
        Watchlist.objects.create(user=request.user, anime_id=anime_id)
        messages.success(request, 'Successfully added to watchlist')
    return redirect('anime:details', anime_id=anime_id)



@login_required
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    animes = []
    for item in watchlist_items:
        response = requests.get(f"{BASE_URL}{item.anime_id}")
        if response.status_code == 200:
            animes.append(response.json()['data'])
    return render(request, 'watchlist.html', {'animes': animes})


@login_required
def remove_from_watchlist(request, anime_id):
    Watchlist.objects.filter(user=request.user, anime_id=anime_id).delete()
    return redirect('watchlist:watchlist')


def empty_watchlist(request):
    Watchlist.objects.filter(user=request.user).delete()
    return redirect('watchlist:watchlist')
