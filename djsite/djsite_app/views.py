from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from .models import Game

menu = ['О сайте', 'Рассылка', 'Вход', 'Предложить идею']


def index(request):
    information = Game.objects.all()
    paginator = Paginator(information, 21)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'djsite_app/index.html', {'page_obj': page_obj, 'title': 'Главная страница', 'information': information, 'menu':menu})


def pageNotFound(request, exception):
    return HttpResponseNotFound('Ошибка 404')