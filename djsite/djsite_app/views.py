from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from .models import Game

menu = ['О сайте', 'Рассылка', 'Вход', 'Предложить идею']


def index(request):
    information = Game.objects.all()
    return render(request, 'djsite_app/index.html', {'title': 'Главная страница', 'information': information, 'menu':menu})


def pageNotFound(request, exception):
    return HttpResponseNotFound('Ошибка 404')