from django.urls import path
from news import views

app_name = 'news'

urlpatterns = [
    path('<int:anime_id>/', views.anime_news, name='news'),
]