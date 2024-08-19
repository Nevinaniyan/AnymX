import requests

BASE_URL = "https://api.jikan.moe/v4/"


def fetch_anime_statistics(anime_id):
    response = requests.get(f"{BASE_URL}anime/{anime_id}/statistics")
    response.raise_for_status()
    return response.json()


