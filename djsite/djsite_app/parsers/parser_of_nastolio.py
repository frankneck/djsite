import os
import re
import django
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException

# Установка переменной окружения для настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsite.settings")
django.setup()

from djsite_app.models import Game

urls = []


def scrape_games_data_nastolio(last_page):

    base_url = 'https://nastol.io/games'
    games_data = []
    price_list = []
    price_list_real = []
    age = []
    time = ""
    age_list = []
    price = ""
    count = 0

    print(f"Total pages: {last_page}")

    for i in range(1, last_page + 1):
        url = base_url if i == 1 else f'{base_url}?page={i}'
        response = requests.get(url)  # Получение экземпляра HTML страницы
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')  # Парсинг страницы
        game_links = soup.find_all('a', class_='hexagon-list-item')  # Их много

        # Проход по всем полученным ссылкам (список артикулов)
        urls = []
        for game_link in game_links:
            game_url = game_link.get('href')
            urls.append(game_url)

        # Проходим по списку ссылок артикулов
        for url in urls:
            # Стек переменных
            vendor = ""
            number_of_players = ""
            number_of_players_list = []

            response = requests.get(url)
            response.encoding = 'utf-8'
            html = response.text

            soup = BeautifulSoup(html, 'html.parser')

            # Получение названия
            title_tag = soup.find('h1', class_='games-one-info__title')
            title = title_tag.text.replace("\n", "").strip()
            title = re.sub(
                r'\s*\((?=.*?(\s*|2021|2020|2019|2018|2017|2016|2015|2014|2013|2012|2011)).*?\)',
                '', title,
                flags=re.IGNORECASE)
            title = title.replace("Головоломка", "").strip()

            # Получение описания
            description_tag = soup.find('main', class_='content-container__main')
            description = description_tag.find_all("div", class_='content-block')
            for description in description:
                description = description.text.replace("\n", "").strip()

            # Получение возраста
            info_tags = soup.find_all('dl', class_='game-one-info__list')
            for info_tag in info_tags:
                age_tags = info_tag.find_all('dd', class_='game-one-info__list-value')  # Находим "куски" с нужной инфой

                for age_tag in age_tags:
                    age_text = age_tag.text.replace("\n", "").strip()
                    age_text = age_text.replace(",", "").strip()
                    age_list = age_text.split()
                    if len(age_list) == 1 and age_list[0].count("+") == 1:
                        age = age_list[0]
                    else:
                        continue

            # Получение изображения
            photo_tag = soup.find('img', class_='games-main-image__img')
            if photo_tag:
                photo = photo_tag.get('src')
            else:
                photo = "Изображение не найдено"

            # Время игры
            for info_tag in info_tags:
                time_tags = info_tag.find_all('dd', class_='game-one-info__list-value')  # Находим "куски" с нужной инфой

                for time_tag in time_tags:
                    time_text = time_tag.text.replace("\n", "").strip()
                    time_text = time_text.replace(",", "").strip()
                    time_list = time_text.split()
                    if len(time_list) == 4 and time_list[1] == "—":
                        time = time_list[0] + " " + time_list[1] + " " + time_list[2] + " " + time_list[3]
                    else:
                        continue

            # Получение кол-ва игроков
            for info_tag in info_tags:
                number_of_players_tags = info_tag.find_all('dd', class_='game-one-info__list-value')  # Находим "куски" с нужной инфой

                for number_of_players_tag in number_of_players_tags:
                    number_of_players_text = number_of_players_tag.text.replace("\n", "").strip()
                    number_of_players_text = number_of_players_text.replace(",", "").strip()
                    number_of_players_list = number_of_players_text.split()
                    if len(number_of_players_list) == 3 and number_of_players_list[1] == "—":
                        number_of_players = number_of_players_list[0] + " - " + number_of_players_list[2] + " " + "игроков"
                    else:
                        continue

            # Создание словаря
            product_data = {
                'Название': title,
                'Описание': description,
                'Цена': price,
                'Изображение': photo,
                'Количество игроков': number_of_players,
                'URL': url,
                'Возраст': age,
                'Время игры': time,
                'Производитель': vendor
            }
            print(product_data)
            games_data.append(product_data)

        return games_data


# scrape_games_data_nastolio(2)
