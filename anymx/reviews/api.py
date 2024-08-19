import requests

BASE_URL = "https://api.jikan.moe/v4/"

def fetch_anime_reviews(anime_id):
    response = requests.get(f"{BASE_URL}anime/{anime_id}/reviews")
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()
