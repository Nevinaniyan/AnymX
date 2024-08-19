
from django.urls import path
from manga import views

app_name = 'manga'

urlpatterns = [
    path('', views.all_manga, name="all_manga"),
    path('details/<int:manga_id>/', views.manga_details, name="manga_details"),
    path('characters/more/<int:manga_id>/', views.more_character, name="more_characters"),
    path('characters/<int:character_id>/', views.character_details, name="character_details"),
    path('posters/<int:manga_id>/', views.manga_pictures, name="manga_pictures"),

]
