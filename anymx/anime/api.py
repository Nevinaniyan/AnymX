import requests

BASE_URL = "https://api.jikan.moe/v4/"


def get_all_anime(anime_id):
    response = requests.get(f"{BASE_URL}anime/{anime_id}")
    response.raise_for_status()
    return response.json()['data']


def get_anime(page=1, limit=24):
    response = requests.get(f"{BASE_URL}top/anime",params={'page': page, 'limit': limit})  # Constructs the full URL using f-string
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()  # Convert the JSON response to a dictionary


def get_anime_details(anime_id):
    try:
        response = requests.get(f"{BASE_URL}anime/{anime_id}/full")
        response.raise_for_status()
        anime_data = response.json()['data']

        # To display characters
        response_characters = requests.get(f"{BASE_URL}anime/{anime_id}/characters")
        response_characters.raise_for_status()
        characters_data = response_characters.json()['data']

        # Adding characters_data to anime_data
        anime_data['characters'] = characters_data

        return anime_data
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return {'data': {}}


def get_character_details(character_id):
    response = requests.get(f"{BASE_URL}characters/{character_id}/full")
    response.raise_for_status()
    return response.json()['data']


def get_anime_pictures(anime_id):
    response = requests.get(f"{BASE_URL}anime/{anime_id}/pictures")
    response.raise_for_status()
    return response.json()['data']


def get_anime_episodes(anime_id, page=1):
    response = requests.get(f"{BASE_URL}anime/{anime_id}/episodes",params={'page': page})
    response.raise_for_status()
    return response.json()


def get_anime_themes(anime_id):
    response = requests.get(f"{BASE_URL}anime/{anime_id}/themes")
    response.raise_for_status()
    return response.json().get('data', {})


def get_anime_streaming(anime_id):
    response = requests.get(f"{BASE_URL}anime/{anime_id}/streaming")
    response.raise_for_status()
    return response.json()['data']


def get_trending_anime(page=1, limit=24):
    response = requests.get(f"{BASE_URL}seasons/now",params={'page': page, 'limit': limit})
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()  # Convert the JSON response to a dictionary


# def get_anime_recommendations():
#     response = requests.get(f"{BASE_URL}recommendations/anime")
#     data = response.json()
#     return data.get('data', [])


# def get_manga_recommendations():
#     response = requests.get(f"{BASE_URL}recommendations/manga")
#     data = response.json()
#     return data.get('data', [])




# f String Literal (f-string):

# The f before the string indicates that it is an f-string (formatted string literal).
# F-strings are a way to embed expressions inside string literals, using curly braces {}.

# {BASE_URL}:
# The expression inside the curly braces {} is evaluated and its result is formatted into the string.
# BASE_URL is a variable that holds the base URL of the API, defined as:
# BASE_URL = "https://api.jikan.moe/v4/"


# Combining the Strings:
# The f-string f"{BASE_URL}top/anime" combines the value of BASE_URL with the string "top/anime".
# When the f-string is evaluated, {BASE_URL} is replaced with its value, resulting in the final string:
