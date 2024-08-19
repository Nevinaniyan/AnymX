from django.shortcuts import render
import requests
from search.forms import SearchForm
from django.core.paginator import Paginator

# Base URL: https://api.jikan.moe/v4/anime is the endpoint for fetching anime data.
# Query Parameters: Adding ?q={query} to the URL allows us to perform a search by including
# the search term dynamically in the request.


# def search_view(request):
#     form = SearchForm(request.GET or None)
#     results = []
#     page_results = None  # page_results is always set even if form is not valid.
#
#     if form.is_valid():
#         query = form.cleaned_data['query']
#         # Calling the Jikan API to get search results
#         response = requests.get(f'https://api.jikan.moe/v4/anime?q={query}')  # Sends a GET request to the Jikan API to search for anime based on the query.
#         if response.status_code == 200:
#             results = response.json().get('data', [])  # Parses the JSON response from the API and extracts the list of anime data. If 'data' is not present, it defaults to an empty list.
#             paginator = Paginator(results, 24)  # Show 24 results per page
#             page_number = request.GET.get('page')  # gets the current page number
#             page_results = paginator.get_page(page_number)  # retrieves the results for the page
#
#     return render(request, 'search_results.html', {'form': form, 'page_results': page_results})



# explanation

# SearchForm(request.GET or None): This line creates an instance of SearchForm using the GET -
# parameters from the request (i.e., the search query entered by the user). -
# If no query is provided, it creates an empty form.

# request.GET contains the get parameter from the url .
# eg:/search/?query=Naruto, request.GET will have {'query':'Naruto'}. If none , returns empty.
# query = form.cleaned_data['query']: Retrieves the cleaned data from the form.
# cleaned_data contains the validated input from the form. Here, query will hold the search term entered by the user.

# response = requests.get(f'https://api.jikan.moe/v4/anime?q={query}')

# basic structure --> https://api.example.com/endpoint?parameter=value

# components --> Base URL: https://api.example.com/endpoint
# Query String: ?parameter=value

# The ? separates the base URL from the query string. Everything following the ? is the query string.

# q is the parameter and query is the value.

# after filtering

def search_view(request):
    form = SearchForm(request.GET or None)
    results = []
    is_manga = False  # set false for anime

    if form.is_valid():
        query = form.cleaned_data['query']

        try:
            # Calling the Jikan API to get search results
            response = requests.get(f'https://api.jikan.moe/v4/anime', params={
                'q': query,
                'limit': 24,
                'order_by': 'popularity',
                'sort': 'asc'
            })
            response.raise_for_status()
            data = response.json()

            explicit_genre_keywords = {'hentai', 'erotic', 'explicit', 'ecchi'}  # explicit keywords

            # Filtering out explicit content based on genre names
            results = [
                anime for anime in data.get('data', [])
                if (
                    not any(explicit_genre_keywords & {genre['name'].lower() for genre in anime.get('genres', [])})
                    and (anime.get('score') or 0) > 0
                    and (anime.get('favorites') or 0) > 0
                    and (anime.get('rank') or 0) > 0
                    and (anime.get('popularity') or 0) > 0
                    and (anime.get('scored_by') or 0) > 0
                )
            ]

        except requests.exceptions.RequestException as e:
            return render(request, 'error.html', {'error_message': f"Error fetching data: {e}"})

    return render(request, 'search_results.html', {
        'form': form,
        'results': results,
        'is_manga': is_manga
    })

# after pagination and filtering

# def search_view(request):
#     form = SearchForm(request.GET or None)
#     results = []
#     page_results = None
#     pagination_info = {}  # Initialize pagination_info
#
#     if form.is_valid():
#         query = form.cleaned_data['query']
#         page = request.GET.get('page', 1)  # Get the page number from the request
#
#         try:
#             # Calling the Jikan API to get search results
#             response = requests.get(f'https://api.jikan.moe/v4/anime', params={'q': query, 'page': page, 'limit': 24})
#             response.raise_for_status()
#             data = response.json()
#
#             explicit_genre_keywords = {'hentai', 'erotic', 'explicit'}  # explicit keywords
#
#             # Filtering out explicit content based on genre names
#             results = [
#                 anime for anime in data.get('data', [])
#                 if not any(explicit_genre_keywords & {genre['name'].lower() for genre in anime.get('genres', [])})
#             ]
#
#             pagination_info = {
#                 'current_page': data['pagination']['current_page'],
#                 'has_next_page': data['pagination']['has_next_page'],
#                 'has_previous_page': data['pagination']['current_page'] > 1,
#                 'last_visible_page': data['pagination']['last_visible_page']
#             }
#
#             # Assign filtered results to page_results
#             page_results = results
#
#         except requests.exceptions.RequestException as e:
#             return render(request, 'error.html', {'error_message': f"Error fetching data: {e}"})
#
#     return render(request, 'search_results.html', {
#         'form': form,
#         'page_results': page_results,
#         'pagination_info': pagination_info
#     })


def manga_search_view(request):
    form = SearchForm(request.GET or None)
    result = []
    is_manga = True  # Set is_manga for manga

    if form.is_valid():
        query = form.cleaned_data['query']

        try:
            response = requests.get(f'https://api.jikan.moe/v4/manga', params={
                'q': query,
                'limit': 24,
                'order_by': 'popularity',
                'sort': 'asc'
            })
            response.raise_for_status()
            data = response.json()

            explicit_genre_keywords = {'hentai', 'erotic', 'explicit', 'ecchi'}
            result = [
                manga for manga in data.get('data', [])
                if (
                    not any(explicit_genre_keywords & {genre['name'].lower() for genre in manga.get('genres', [])})
                    and (manga.get('score') or 0) > 0
                    and (manga.get('favorites') or 0) > 0
                    and (manga.get('rank') or 0) > 0
                    and (manga.get('popularity') or 0) > 0
                    and (manga.get('scored_by') or 0) > 0
                )
            ]

        except requests.exceptions.RequestException as e:
            return render(request, 'error.html', {'error_message': f"Error fetching data: {e}"})

    return render(request, 'manga_search_results.html', {
        'form': form,
        'result': result,
        'is_manga': is_manga
    })


