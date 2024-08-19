from django.shortcuts import render
import requests
from news.api import get_anime_news


def anime_news(request, anime_id):
    try:
        news = get_anime_news(anime_id)
    except requests.exceptions.HTTPError as e:
        # Handle error or provide a fallback
        news = []

    context = {
        'news': news,
        'anime_id': anime_id,
    }
    return render(request, 'anime_news.html', context)
