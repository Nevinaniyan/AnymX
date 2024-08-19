import requests
from django.core.paginator import Paginator
from django.shortcuts import render
from anime.api import get_all_anime, get_anime, get_anime_details, get_character_details, get_anime_pictures, get_anime_episodes, get_anime_themes, get_anime_streaming, get_trending_anime
from reviews.models import Review
from favourites.models import Favourite
from watchlist.models import Watchlist

BASE_URL = "https://api.jikan.moe/v4/anime"


def all_page(request):
    return render(request,'all_page.html')


def home(request):
    page = request.GET.get('page', 1)  # Get the page number from the request
    try:
        response = requests.get(BASE_URL, params={
            'page': page,
            'limit': 24,
            'order_by': 'popularity',
            'sort': 'asc'
        })
        response.raise_for_status()
        data = response.json()

        explicit_genre_keywords = {'hentai', 'erotic', 'ecchi'}  # explicit keywords

        # Filtering out explicit content based on genre names
        anime_list = [
            anime for anime in data['data']
            if (
                not any(explicit_genre_keywords & {genre['name'].lower() for genre in anime.get('genres', [])})
                and (anime.get('score') or 0) > 0
                and (anime.get('favorites') or 0) > 0
                and (anime.get('rank') or 0) > 0
                and (anime.get('popularity') or 0) > 0
                and (anime.get('scored_by') or 0) > 0
            )
        ]

        pagination_info = {
            'current_page': data['pagination']['current_page'],
            'has_next_page': data['pagination']['has_next_page'],
            'has_previous_page': data['pagination']['current_page'] > 1,
            'last_visible_page': data['pagination']['last_visible_page']
        }

        return render(request, 'home.html', {
            'anime_list': anime_list,
            'pagination_info': pagination_info
        })

    except requests.exceptions.RequestException as e:
        return render(request, 'error.html', {'error_message': f"Error fetching data: {e}"})


def welcome(request):
    return render(request, 'welcome.html')


# def top_anime(request):
#     data = get_anime()       # After calling get_anime(), the returned JSON data is stored in the variable data:
#     top_anime = data['data']  # To access the list of anime entries within this data, you use data['data']:
#     # data is the dictionary obtained from response.json().
#     # data['data'] accesses the value associated with the key 'data', which is a list of anime entries.
#     return render(request, 'top_anime.html', {'top_anime': top_anime})


def top_anime(request):
    page = request.GET.get('page', 1)
    try:
        data = get_anime(page)

        anime_list = data['data']

        # List of known explicit genre keywords
        explicit_genre_keywords = {'hentai', 'erotic','ecchi'}

        # Filter out explicit content based on genre names
        top_anime = [
            anime for anime in anime_list
            if (
                not any(explicit_genre_keywords & {genre['name'].lower() for genre in anime.get('genres', [])})
                and (anime.get('score') or 0) > 0
                and (anime.get('favorites') or 0) > 0
                and (anime.get('rank') or 0) > 0
                and (anime.get('popularity') or 0) > 0
                and (anime.get('scored_by') or 0) > 0
            )
        ]

        pagination_info = {
            'current_page': data['pagination']['current_page'],
            'has_next_page': data['pagination']['has_next_page'],
            'has_previous_page': data['pagination']['current_page'] > 1,
            'last_visible_page': data['pagination']['last_visible_page']
        }

        return render(request, 'top_anime.html', {
            'top_anime': top_anime,
            'pagination_info': pagination_info
        })

    except requests.exceptions.RequestException as e:
        return render(request, 'error.html', {'error_message': f"Error fetching data: {e}"})


def trending_animes(request):
    page = request.GET.get('page', 1)
    try:
        data = get_trending_anime(page)

        anime_list = data['data']

        # List of known explicit genre keywords
        explicit_genre_keywords = {'hentai', 'erotic', 'ecchi'}

        # Filter out explicit content based on genre names
        trending_anime = [
            anime for anime in anime_list
            if (
                not any(explicit_genre_keywords & {genre['name'].lower() for genre in anime.get('genres', [])})
                and (anime.get('score') or 0) > 0
                and (anime.get('favorites') or 0) > 0
                and (anime.get('rank') or 0) > 0
                and (anime.get('popularity') or 0) > 0
                and (anime.get('scored_by') or 0) > 0
            )
        ]

        pagination_info = {
            'current_page': data['pagination']['current_page'],
            'has_next_page': data['pagination']['has_next_page'],
            'has_previous_page': data['pagination']['current_page'] > 1,
            'last_visible_page': data['pagination']['last_visible_page']
        }

        return render(request, 'trending_anime.html', {
            'trending_anime': trending_anime,
            'pagination_info': pagination_info,
        })

    except requests.exceptions.RequestException as e:
        return render(request, 'error.html', {'error_message': f"Error fetching data: {e}"})

# def anime_detail(request, anime_id):
#     try:
#         anime = get_anime_details(anime_id)
#         streaming_links = get_anime_streaming(anime_id)
#         characters = anime.get('characters', [])
#         visible_characters = characters[:20]  # Limit to 20 characters on the page
#         total_characters = len(characters)
#     except requests.RequestException as e:
#         print(f"Request error: {e}")
#         anime = {}
#         streaming_links = []
#         visible_characters = []
#         total_characters = 0
#
#     context = {
#         'anime': anime,
#         'streaming': streaming_links,
#         'visible_characters': visible_characters,
#         'total_characters': total_characters,
#     }
#     return render(request, 'anime_details.html', context)


# for review

def anime_detail(request, anime_id):
    try:
        anime = get_anime_details(anime_id)
        streaming_links = get_anime_streaming(anime_id)
        characters = anime.get('characters', [])
        visible_characters = characters[:20]  # Limit to 20 characters on the page
        total_characters = len(characters)

        # Fetch reviews for the anime
        reviews = Review.objects.filter(anime_id=anime_id)
    except requests.RequestException as e:
        print(f"Request error: {e}")
        anime = {}
        streaming_links = []
        visible_characters = []
        total_characters = 0
        reviews = []

    context = {
        'anime': anime,
        'streaming': streaming_links,
        'visible_characters': visible_characters,
        'total_characters': total_characters,
        'reviews': reviews,
    }
    return render(request, 'anime_details.html', context)

# after review, favourites, and watchlist



def more_characters(request, anime_id):
    try:
        anime = get_anime_details(anime_id)
        characters = anime.get('characters', [])
    except requests.RequestException as e:
        print(f"Request error: {e}")
        characters = []

    context = {
        'anime': anime,
        'characters': characters,
    }
    return render(request, 'more_characters.html', context)


def character_details(request,character_id):
    character = get_character_details(character_id)
    return render(request, 'character_details.html',{'character': character})


def anime_pictures(request, anime_id):
    try:
        anime = get_anime_details(anime_id)
        pictures = get_anime_pictures(anime_id)
    except requests.RequestException as e:
        print(f"Request error: {e}")
        pictures = {}

    context = {
        'anime': anime,
        'pictures': pictures,
        'anime_id': anime_id,

    }
    return render(request, 'anime_media.html', context)


def anime_episodes(request, anime_id):
    page = int(request.GET.get('page', 1))  # Get the current page from the query parameters
    try:
        anime = get_anime_details(anime_id)
        episodes_data = get_anime_episodes(anime_id, page)
        episodes = episodes_data.get('data', [])
        pagination_info = episodes_data.get('pagination', {})
    except requests.RequestException as e:
        print(f"Request error: {e}")
        anime = {}
        episodes = []

        pagination_info = {
            # 'current_page': episodes['pagination']['current_page'],
            # 'has_next_page': episodes['pagination']['has_next_page'],
            # 'has_previous_page': episodes['pagination']['current_page'] > 1,
            # 'last_visible_page': episodes['pagination']['last_visible_page']
        }

    context = {
        'episodes': episodes,
        'anime_id': anime_id,
        'pagination_info': pagination_info,
        'anime': anime,
    }
    return render(request, 'anime_episodes.html', context)


def anime_themes(request, anime_id):
    try:
        anime = get_anime_details(anime_id)
        themes = get_anime_themes(anime_id)
    except requests.RequestException as e:
        print(f"Request error: {e}")
        themes = {'openings': [], 'endings': []}
        anime = {}

    context = {
        'themes': themes,
        'anime': anime,
    }
    return render(request, 'anime_themes.html', context)


def recommendation_page(request):
    return render(request,'recommendation.html')


# def recommendation_page(request):
#     anime_recommendations = get_anime_recommendations()
#     manga_recommendations = get_manga_recommendations()
#
#     explicit_genre_keywords = {'hentai', 'erotic'}  # Explicit content genres
#     explicit_title_keywords = {'hentai', 'ecchi', 'ero', 'adult'}  # Explicit content in titles
#
#     def is_explicit(entry):
#         genres = {genre['name'].lower() for genre in entry.get('genres', [])}
#         title = entry.get('title', '').lower()
#         return (
#             explicit_genre_keywords & genres or
#             any(keyword in title for keyword in explicit_title_keywords)
#         )
#
#     # Filtering anime recommendations
#     filtered_anime = [
#         anime for anime in anime_recommendations
#         if all(not is_explicit(entry) for entry in anime.get('entry', []))
#     ]
#
#     # Filtering manga recommendations
#     filtered_manga = [
#         manga for manga in manga_recommendations
#         if all(not is_explicit(entry) for entry in manga.get('entry', []))
#     ]
#
#     # Paginate anime recommendations
#     paginator = Paginator(filtered_anime, 10)  # 10 anime per page
#     page_number = request.GET.get('page')
#     anime_page_obj = paginator.get_page(page_number)
#
#     # Paginate manga recommendations
#     manga_paginator = Paginator(filtered_manga, 10)  # 10 manga per page
#     manga_page_number = request.GET.get('manga_page')
#     manga_page_obj = manga_paginator.get_page(manga_page_number)
#
#     # Pass paginated objects to the context
#     context = {
#         'anime_page_obj': anime_page_obj,
#         'manga_page_obj': manga_page_obj,
#     }
#
#     return render(request, 'recommendation.html', context)

