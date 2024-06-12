from django.db import models
from django.utils.text import slugify
import os


class Game(models.Model):
    title = models.CharField(max_length=100) #Лавка орка
    description = models.TextField(blank=True) #Лавка орка
    photo = models.URLField() #Лавка орка
    vendor = models.CharField(max_length=100) #Лавка орка
    year = models.IntegerField() #Hobby Games
    price = models.IntegerField() #Лавка орка Hobby Games Вообще было бы прикольно низкую выводить
    number_of_players = models.CharField(max_length=10) #Hobby Games

    def __str__(self):
        return self.title
