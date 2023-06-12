from django.db import models
from QGame import *


class Player(models.Model):
    name = models.CharField(max_length=100)


class Game(models.Model):
    def __init__(self):
        self.game = QGame()
