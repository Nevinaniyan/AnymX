
from django.contrib import admin
from django.urls import path,include
from anime import views
from django.conf import settings                       # to display media content
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),   # built-in authentication urls
    # path('', include('users.urls')),
    path('',views.welcome,name="welcome"),
    path('anime/',include('anime.urls')),
    path('manga/',include('manga.urls')),
    path('reviews/',include('reviews.urls')),
    path('favourites/',include('favourites.urls')),
    path('search/',include('search.urls')),
    path('',include('users.urls')),
    path('watchlist/',include('watchlist.urls')),
    path('news/',include('news.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
