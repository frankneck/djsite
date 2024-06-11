from django.db import models
from django.utils.text import slugify
import os


class Game(models.Model):

    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("ArticleSeries", slugify(self.article_slug), instance)
        return None

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.URLField()
    category = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.IntegerField()
    number_of_players = models.CharField(max_length=10)
    age = models.CharField(max_length=10)

    def __str__(self):
        return self.title
