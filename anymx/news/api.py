import requests

BASE_URL = 'https://api.jikan.moe/v4/'


def get_anime_news(anime_id):
    response = requests.get(f"{BASE_URL}anime/{anime_id}/news")
    response.raise_for_status()
    return response.json()['data']
