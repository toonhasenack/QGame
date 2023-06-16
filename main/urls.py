from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.main_page),
    path('game/<int:player_id>/', views.game_page),
    path('game/<int:player_id>/winner/', views.winner_page)
]
