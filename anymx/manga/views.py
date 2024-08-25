from django.shortcuts import render
import requests
from manga.api import get_all_manga, get_manga_details, get_character_details, get_manga_pictures

BASE_URL = "https://api.jikan.moe/v4/manga"


def all_manga(request):
    page = int(request.GET.get('page', 1))
    max_pages = 999

    if page > max_pages:
        page = max_pages  # Get the page number from the request
    try:
        response = requests.get(BASE_URL, params={
            'page': page,
            'limit': 24,
            'order_by': 'scored_by',
            'sort': 'desc'
        })
        response.raise_for_status()
        data = response.json()

        explicit_genre_keywords = {'hentai', 'erotic', 'ecchi'}  # explicit keywords

        # Filtering out explicit content based on genre names
        manga_list = [
            manga for manga in data['data']
            if (
               not any(explicit_genre_keywords & {genre['name'].lower() for genre in manga.get('genres', [])})
               and (manga.get('score') or 0) > 0
               and (manga.get('favorites') or 0) > 0
               and (manga.get('rank') or 0) > 0
               and (manga.get('popularity') or 0) > 0
               and (manga.get('scored_by') or 0) > 0
            )
        ]

        total_pages = min(data['pagination']['last_visible_page'], max_pages)
        pagination_info = {
            'current_page': page,
            'has_next_page': page < total_pages and data['pagination']['has_next_page'],
            'has_previous_page': page > 1,
            'last_visible_page': total_pages
        }

        return render(request, 'all_manga.html', {
            'manga_list': manga_list,
            'pagination_info': pagination_info,

        })

    except requests.exceptions.RequestException as e:
        return render(request, 'error.html', {'error_message': f"Error fetching data: {e}"})


def manga_details(request, manga_id):
    try:
        manga = get_manga_details(manga_id)
        characters = manga.get('characters', [])
        visible_characters = characters[:20]  # Limit to 20 characters on the page
        total_characters = len(characters)
    except requests.RequestException as e:
        print(f"Request error: {e}")
        manga = {}
        visible_characters = []
        total_characters = 0

    context = {
        'manga': manga,
        'visible_characters': visible_characters,
        'total_characters': total_characters,
    }
    return render(request, 'manga_details.html', context)


def more_character(request, manga_id):
    try:
        manga = get_manga_details(manga_id)
        characters = manga.get('characters', [])
    except requests.RequestException as e:
        print(f"Request error: {e}")
        characters = []

    context = {
        'manga': manga,
        'characters': characters,

    }
    return render(request, 'more_character.html', context)


def character_details(request, character_id):
    character = get_character_details(character_id)
    return render(request, 'character_detail.html', {'character': character})


def manga_pictures(request, manga_id):
    try:
        manga = get_manga_details(manga_id)
        picture = get_manga_pictures(manga_id)
    except requests.RequestException as e:
        print(f"Request error: {e}")
        picture = {}

    context = {
        'picture': picture,
        'manga_id': manga_id,
        'manga': manga,
    }
    return render(request, 'manga_media.html', context)

