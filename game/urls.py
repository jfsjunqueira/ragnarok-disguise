from django.urls import path
from . import views

from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
    path('', views.start, name='start'),
    path('game/', views.game, name='game'),
    path('game_over/', views.game_over, name='game_over'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
