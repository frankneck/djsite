from django.db import models
from django.utils.text import slugify
import os


class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    photo = models.URLField()
    vendor = models.CharField(max_length=100)
    price = models.IntegerField()
    age = models.CharField(max_length=255, blank=True, null=True, default=None)
    number_of_players = models.CharField(max_length=10)
    time = models.CharField(max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        return self.title
