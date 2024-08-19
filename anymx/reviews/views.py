import requests
from django.shortcuts import render, get_object_or_404, redirect
from reviews.api import fetch_anime_reviews
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reviews.models import Review
from reviews.forms import ReviewForm
from anime.api import get_anime_details


def anime_reviews(request, anime_id):
    try:
        data = fetch_anime_reviews(anime_id)
        anime = get_anime_details(anime_id)
        reviews = data['data']
    except requests.HTTPError as e:
        reviews = []
        anime = []

    paginator = Paginator(reviews, 10)

    page = request.GET.get('page', 1)
    try:
        reviews_page = paginator.page(page)
    except PageNotAnInteger:
        reviews_page = paginator.page(1)
    except EmptyPage:
        reviews_page = paginator.page(paginator.num_pages)

    return render(request, 'anime_reviews.html', {'reviews': reviews_page, 'anime': anime})


# @login_required
# def add_review(request, anime_id):
#     user = request.user
#     try:
#         anime = get_anime_details(anime_id)
#     except requests.RequestException as e:
#         print(f"Request error: {e}")
#         anime = {}
#
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.anime_id = anime_id
#             review.user = user
#             review.save()
#             return redirect('anime:details', anime_id=anime_id)
#     else:
#         form = ReviewForm()
#
#     return render(request, 'add_review.html', {'form': form, 'anime': anime})


# add review with message for integrity error
@login_required()
def add_review(request, anime_id):
    user = request.user
    try:
        anime = get_anime_details(anime_id)
    except requests.RequestException as e:
        print(f"Request error: {e}")
        anime = {}

    # Check if the user has already reviewed this anime
    if Review.objects.filter(anime_id=anime_id, user=user).exists():
        messages.warning(request, "You have already reviewed this anime.")
        return redirect('anime:details', anime_id=anime_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.anime_id = anime_id
            review.user = user
            review.save()
            messages.success(request, "Your review has been added.")
            return redirect('anime:details', anime_id=anime_id)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'anime': anime})


def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    anime_id = review.anime_id  # Get the anime ID to redirect after deletion
    review.delete()
    return redirect('anime:details', anime_id=anime_id)