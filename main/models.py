from django.db import models

# Create your models here.
from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    publication_date = models.DateField()
