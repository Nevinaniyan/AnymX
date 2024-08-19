from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login_user, name="login"),
    path('profile/', views.profile, name="profile"),
    path('profileUpdate/', views.profile_update, name="profile_update"),
    path('logout/', views.logout_user, name="logout"),

]