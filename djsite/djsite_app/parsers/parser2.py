import re
import os
import django
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException

# Установка переменной окружения для настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsite.settings")
django.setup()

from djsite_app.models import Game

def scrape_games_data(last_page):
    base_url = 'https://www.mosigra.ru/nastolnye-igry'
    try:
        html = requests.get(base_url, timeout=10).text
    except RequestException as e:
        print(f"Error fetching base URL: {e}")
        return []

    soup = BeautifulSoup(html, 'html.parser')

    print(f"Total pages: {last_page}")
    urls = []
    games_data = []

    # Collect game URLs from each page
    for i in range(1, last_page):
        url = base_url if i == 1 else f'{base_url}?page={i}'

        try:
            html = requests.get(url, timeout=10).text
        except RequestException as e:
            print(f"Error fetching page {i}: {e}")
            continue

        soup = BeautifulSoup(html, 'html.parser')
        game_links = soup.find_all('a', class_='card__image ')

        for link in game_links:
            game_url = link.get('href')
            urls.append(game_url)

    print(f"Total game URLs collected: {len(urls)}")

    # Fetch game details from each URL
    for url in urls:
        try:
            html = requests.get(url, timeout=10).text
        except RequestException as e:
            print(f"Error fetching game URL {url}: {e}")
            continue

        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('article', class_='product__article tabs-container')
        photo_url_tag = soup.find('img', itemprop='image')
        price_tag = soup.find('b', class_='h1')
        description_tag = soup.find('section', class_='tab-pane fade show active')
        age_tag = soup.find('section', id='attributes')
        vendor_tag = soup.find('section', id='attributes')

        title = (title_tag.text.strip().replace("Настольная игра", "").strip()
                 if title_tag else "Название не найдено")

        description = (description_tag.get_text(separator='\n').strip().replace('\n', ' ').lstrip(' ')
                       if description_tag else "Описание не найдено")

        photo_url = photo_url_tag.get('src') if photo_url_tag else "Изображение не найдено"

        price = price_tag.get_text().replace(" ", "").strip() if price_tag else "Цена не найдена"

        age = (age_tag.get_text().replace("\n", " ").strip().replace("Возраст", "").strip()
               if age_tag else "Возраст не найден")
        age = age.split(', ')
        if len(age) >= 2:
            age = str(age[0] + "+")
        else:
            age = age[-1] + "+"

        vendor = vendor_tag.get_text().strip()

        product_data = {
            'Название': title,
            'Описание': description,
            'Цена': price,
            'Изображение': photo_url,
            'URL': url,
            'Возраст': age
        }
        games_data.append(product_data)

    return games_data

def save_games_to_database(games_data):
    for game_data in games_data:
        game, created = Game.objects.get_or_create(
            url=game_data['URL'],
            defaults={
                'title': game_data['Название'],
                'description': game_data['Описание'],
                'photo': game_data['Изображение'],
                'price': int(game_data['Цена']) if game_data['Цена'].isdigit() else 0,
                'age': game_data['Возраст']
            }
        )

        if not created:
            fields_to_update = False
            if not game.title:
                game.title = game_data['Название']
                fields_to_update = True
            if not game.description:
                game.description = game_data['Описание']
                fields_to_update = True
            if not game.photo:
                game.photo = game_data['Изображение']
                fields_to_update = True
            if not game.price:
                game.price = int(game_data['Цена']) if game_data['Цена'].isdigit() else 0
                fields_to_update = True
            if not game.age:
                game.age = game_data['Возраст']
                fields_to_update = True

            if fields_to_update:
                game.save()
                print(f"Updated game: {game}")
            else:
                print(f"No updates needed for game: {game}")
        else:
            print(f"Saved new game: {game}")

# В качестве параметра задано кол-во страниц
games = scrape_games_data(35)
save_games_to_database(games)

print(f"Total games scraped: {len(games)}")
