from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


def index(request):
    return HttpResponse("Временная главная страница")  #TO DO


def pageNotFound(request, exception):
    return HttpResponseNotFound('Ошибка 404')