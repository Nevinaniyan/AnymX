import requests

BASE_URL = "https://api.jikan.moe/v4/"


def get_all_manga(manga_id):
    response = requests.get(f"{BASE_URL}manga/{manga_id}")
    response.raise_for_status()
    return response.json()['data']


def get_manga_details(manga_id):
    try:
        response = requests.get(f"{BASE_URL}manga/{manga_id}/full")
        response.raise_for_status()
        manga_data = response.json()['data']

        # To display characters
        response_characters = requests.get(f"{BASE_URL}manga/{manga_id}/characters")
        response_characters.raise_for_status()
        characters_data = response_characters.json()['data']

        # Adding characters_data to manga_data
        manga_data['characters'] = characters_data

        return manga_data
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return {'data': {}}


def get_character_details(character_id):
    response = requests.get(f"{BASE_URL}characters/{character_id}/full")
    response.raise_for_status()
    return response.json()['data']


def get_manga_pictures(manga_id):
    response = requests.get(f"{BASE_URL}manga/{manga_id}/pictures")
    response.raise_for_status()
    return response.json()['data']