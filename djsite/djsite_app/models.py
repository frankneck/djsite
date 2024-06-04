from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    category = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.IntegerField()
    number_of_players = models.CharField(max_length=10)
    age = models.CharField(max_length=10)