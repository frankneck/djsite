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
    # Стек переменных
    base_url = 'https://www.igroved.ru/search/'  # Главная страница сайта для парсинга
    games_data = []
    price_list = []
    price_list_real = []
    price = ""
    count = 0

    # Вывод кол-ва спаршенных страниц
    print(f"Total pages: {last_page}")

    # Проходим по всем страницам сайта (на самом деле первым тысячам)
    for i in range(1, last_page + 1):
        # URL страницы с настолками
        url = base_url if i == 1 else f'{base_url}?page={i}'
        # Получение экземпляра HTML страницы
        response = requests.get(url)
        response.encoding = 'utf-8'
        html = response.text
        # Парсинг страницы
        soup = BeautifulSoup(html, 'html.parser')
        # Поиск всех экземпляров класса "thumbnail"
        game_links = soup.find_all('div', class_='item')  # Их много

        # Проход по всем полученным ссылкам (список артикулов)
        for game_link in game_links:
            game_url = game_link.find('div', class_='thumbnail')
            game_url = game_url.find('a', href=True)  # Находим ссылку на товар
            game_url = game_url.get(
                'href')  # Получение URL артикула и добавление в список артикулов (для получения данных из ссылки)
            game_url = 'https://www.igroved.ru' + game_url

            # Получение цены
            price_tag = game_link.find('div', class_='price-box')
            price_str = price_tag.text.replace("₽", "").strip()
            price_str = price_str.replace("\n", " ")
            price_str = price_str.replace(" ", ",")
            price_list = price_str.split(",")

            if len(price_list) > 3:
                price_list = (price_list[0] + price_list[1] + "," + price_list[-2] + price_list[-1]).split(",")
                price = price_list[1]  # второй элемент это скидочная цена
                price_list_real.append(price)
            elif len(price_list) == 2:
                price = (price_list[0] + price_list[1])
                price_list_real.append(price)
            else:
                price = price_list[0]
                price_list_real.append(price)

            if game_url.find('games') != -1:  # Проверка на наличие в строке "games"
                urls.append(game_url)
            else:
                continue

    count_for_price = 0
    # Проходим по списку ссылок артикулов
    for url in urls:
        # Стек переменных
        time = ""
        age = ""
        vendor = ""
        number_of_players = ""
        number_of_players_list = []

        # Парсинг данных страницы артикула
        response = requests.get(url)
        # Меняем явно кодировку
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # Получение названия
        title_tag = soup.find('header', class_='entry-header')
        title = title_tag.find('h1', itemprop='name').text.replace("Настольная игра", "").strip()
        title = title.replace("-головоломка", "").strip()
        title = title.capitalize()
        # Получение описания
        description = soup.find('div', class_='article-box').text.replace("\n", "").strip()

        # Получение возраста
        age_tags = soup.find('div', class_='properties-box')

        if age_tags:
            age_tags = age_tags.find_all('a', class_='')
        else:
            age_tags = "Возраст не найден"

        for age_tag in age_tags:  # Создание цикла для нахождения нужных данных
            href = age_tag.get('href')

            if href.count("search/?age") > 0:  # Если ссылка из таблицы подходит под условие, то это возраст
                age = age_tag.text
            else:
                continue

        photo_tag = soup.find('a', class_='cbox')
        if photo_tag:
            photo = photo_tag.get('href')
        else:
            photo = "Изображение не найдено"

        # Получение производителя
        vendor_tags = soup.find('div', class_='properties-box')
        if vendor_tags:
            vendor_tag = vendor_tags.find('a', class_='')
            vendor = vendor_tag.text
            if vendor == "на английском языке":  # Проверка: производитель имеется
                continue
            count += 1
        else:
            vendor = "Производитель не найден"

        # Получение кол-ва игроков
        number_of_players_tags = soup.find('div', class_='properties-box')

        if number_of_players_tags:
            number_of_players_tags = number_of_players_tags.find_all('a', class_='')
        else:
            number_of_players_tags = "Кол-во игроков не найдено"

        for number_of_players_tag in number_of_players_tags:
            href = number_of_players_tag.get('href')

            if href.count("search/?numPlayers") > 0:
                number_of_players_list.append(number_of_players_tag.text)
            else:
                continue
        if len(number_of_players_list) > 1:
            number_of_players = number_of_players_list[0] + " " + "игроков"
        else:
            number_of_players = ""

        # Получение длительности игры игроков
        time_tags = soup.find('div', class_='properties-box')
        time_tag_list = []
        if time_tags:
            time_tags = time_tags.find_all('a', class_='')
        else:
            time_tags = "Длительности игры не найдено"

        for time_tag in time_tags:
            href = time_tag.get('href')

            if href.count("search/?numPlayers") > 0:
                time_tag_list.append(time_tag.text)
            else:
                continue
        if len(time_tag_list) > 1:
            time = time_tag_list[1]
        else:
            time = ""

        # Получение цены
        if count_for_price < len(price_list_real):
            price = price_list_real[count_for_price]
            count_for_price += 1
        else:
            price = "Цена не найдена"

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
        games_data.append(product_data)
        print(product_data)
    return games_data


# scrape_games_data_igroved(2)
