from django.urls import path
from .views import signup, login, logout, profile

urlpatterns = [
    path('signup', signup),
    path('login', login),
    path('logout', logout),
    path('profile', profile),
]
