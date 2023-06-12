from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.main_page),
    path('game/', views.game_page)
]
