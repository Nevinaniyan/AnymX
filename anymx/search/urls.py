
from django.urls import path
from search import views

app_name="search"

urlpatterns = [
    path('search/', views.search_view, name="search"),
    path('manga/searching/', views.manga_search_view, name="manga_search")

]
