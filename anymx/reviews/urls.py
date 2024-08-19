
from django.urls import path
from reviews import views

app_name="reviews"

urlpatterns = [
    path('anime/<int:anime_id>/reviews/', views.anime_reviews, name='anime_reviews'),
    path('add/<int:anime_id>/', views.add_review, name='add_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
