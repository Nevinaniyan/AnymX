from django.urls import path
from watchlist import views

app_name="watchlist"

urlpatterns = [
    path('add/<int:anime_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('', views.watchlist, name='watchlist'),
    path('remove/<int:anime_id>/', views.remove_from_watchlist, name='remove'),
    path('empty/', views.empty_watchlist, name='empty_watchlist'),
]
