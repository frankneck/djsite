from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Временная главная страница")  #TO DO
