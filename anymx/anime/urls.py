
from django.urls import path
from anime import views

app_name="anime"

urlpatterns = [
    path('anymX/',views.all_page, name="all_page"),
    path('home/', views.home, name="home"),
    path('top/', views.top_anime, name="top"),
    path('details/<int:anime_id>/', views.anime_detail, name="details"),
    path('media/<int:anime_id>/', views.anime_pictures, name="pictures"),
    path('characters/<int:anime_id>/', views.more_characters, name="more_characters"),
    path('characters/details/<int:character_id>/', views.character_details, name="character_details"),
    path('<int:anime_id>/episodes/', views.anime_episodes, name='anime_episodes'),
    path('<int:anime_id>/themes/', views.anime_themes, name='anime_themes'),
    path('trending/', views.trending_animes, name="trending"),
    path('recommendations/', views.recommendation_page, name="recom"),

]
