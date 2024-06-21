import os
import django
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException

# Установка переменной окружения для настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsite.settings")
django.setup()

from djsite_app.models import Game

urls = []

def scrape_games_data_igroved(last_page):
    base_url = 'https://www.igroved.ru/search/'  # Главная страница сайта для парсинга
    games_data = []
    price_list = []
    price_list_real = []
    price = ""
    count = 0

    print(f"Total pages: {last_page}")

    for i in range(1, last_page + 1):
        url = base_url if i == 1 else f'{base_url}?page={i}'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка наличия ошибок в ответе
        except RequestException as e:
            print(f"Error fetching page {i}: {e}")
            continue

        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        game_links = soup.find_all('div', class_='item')

        for game_link in game_links:
            game_url = game_link.find('div', class_='thumbnail')
            game_url = game_url.find('a', href=True)
            game_url = game_url.get('href')
            game_url = 'https://www.igroved.ru' + game_url

            price_tag = game_link.find('div', class_='price-box')
            price_str = price_tag.text.replace("₽", "").strip().replace("\n", " ").replace(" ", ",")
            price_list = price_str.split(",")

            if len(price_list) > 3:
                price_list = (price_list[0] + price_list[1] + "," + price_list[-2] + price_list[-1]).split(",")
                price = price_list[1]
                price_list_real.append(price)
            elif len(price_list) == 2:
                price = price_list[0] + price_list[1]
                price_list_real.append(price)
            else:
                price = price_list[0]
                price_list_real.append(price)

            if 'games' in game_url:
                urls.append(game_url)
            else:
                continue

    count_for_price = 0
    for url in urls:
        time = ""
        age = ""
        vendor = ""
        number_of_players = ""
        number_of_players_list = []

        try:
            response = requests.get(url)
            response.raise_for_status()
        except RequestException as e:
            print(f"Error fetching game URL {url}: {e}")
            continue

        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        title_tag = soup.find('header', class_='entry-header')
        if title_tag:
            title = title_tag.find('h1', itemprop='name')
            if title:
                title = title.text.replace("Настольная игра", "").strip()
                title = title.replace("-головоломка", "").strip()
                title = title.replace("Головоломка", "").strip()
                title = title.capitalize()
            else:
                title = "Название не найдено"
        else:
            title = "Название не найдено"

        description = soup.find('div', class_='article-box').text.replace("\n", "").strip()

        age_tags = soup.find('div', class_='properties-box')
        if age_tags:
            age_tags = age_tags.find_all('a', class_='')
        else:
            age_tags = []

        for age_tag in age_tags:
            href = age_tag.get('href')
            if 'search/?age' in href:
                age = age_tag.text
                break

        photo_tag = soup.find('a', class_='cbox')
        photo = photo_tag.get('href') if photo_tag else "Изображение не найдено"

        vendor_tags = soup.find('div', class_='properties-box')
        if vendor_tags:
            vendor_tag = vendor_tags.find('a', class_='')
            vendor = vendor_tag.text if vendor_tag else ""
            if vendor == "на английском языке":
                continue
        else:
            vendor = "Производитель не найден"

        number_of_players_tags = soup.find('div', class_='properties-box')
        if number_of_players_tags:
            number_of_players_tags = number_of_players_tags.find_all('a', class_='')
        else:
            number_of_players_tags = []

        for number_of_players_tag in number_of_players_tags:
            href = number_of_players_tag.get('href')
            if 'search/?numPlayers' in href:
                number_of_players_list.append(number_of_players_tag.text)
                break

        number_of_players = number_of_players_list[0] + " игроков" if number_of_players_list else ""

        time_tags = soup.find('div', class_='properties-box')
        time_tag_list = []
        if time_tags:
            time_tags = time_tags.find_all('a', class_='')
        else:
            time_tags = []

        for time_tag in time_tags:
            href = time_tag.get('href')
            if 'search/?numPlayers' in href:
                time_tag_list.append(time_tag.text)
                break

        time = time_tag_list[0] if time_tag_list else ""

        if count_for_price < len(price_list_real):
            price = price_list_real[count_for_price]
            count_for_price += 1
        else:
            price = "Цена не найдена"

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
        games_data.append(product_data)
        print(product_data)
    return games_data

