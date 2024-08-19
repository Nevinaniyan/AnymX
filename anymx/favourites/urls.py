from django.urls import path
from favourites import views

app_name = "favourites"

urlpatterns = [
    path('anime/<int:anime_id>/statistics/', views.anime_statistics, name='anime_statistics'),
    path('add_anime/<int:anime_id>/', views.add_to_favourites_anime, name='add_to_favourites_anime'),
    path('add_character/<int:character_id>/', views.add_to_favourites_character, name='add_to_favourites_character'),
    path('', views.favourites, name='favourites'),
    path('remove/<int:anime_id>/', views.remove_from_favourites, name='remove'),
    path('empty/', views.empty_favourites, name='empty_favourites'),
]
