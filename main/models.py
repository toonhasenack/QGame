from django.db import models


class Player(models.Model):
    name1 = models.CharField(max_length=100)
    name2 = models.CharField(max_length=100)
    grid1 = models.BinaryField(max_length=100, default=b'\x08')
    grid2 = models.BinaryField(max_length=100, default=b'\x08')
    player = models.IntegerField(default=0)
    steps = models.IntegerField(default=0)
    left = models.BooleanField(default=False)
    left_choice = models.BinaryField(max_length=100, default=b'\x08')
    right = models.BooleanField(default=False)
    right_choice = models.BinaryField(max_length=100, default=b'\x08')
    winner = models.IntegerField(default=0)
    message = models.CharField(max_length=100)
    new_id = models.IntegerField(default=0)
