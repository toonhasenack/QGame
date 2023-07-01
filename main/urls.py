from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.main_page),
    path('game/<int:player_id>/', views.game_page),
    path('leaderboard', views.leaderboard_page)
]
