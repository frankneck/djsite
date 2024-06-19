import re
import os
import django
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsite.settings")
django.setup()

from djsite_app.models import Game


def scrape_games_data_goodork(last_page):
    base_url = 'https://goodork.ru/categories/nastolnye-igry'
    try:
        html = requests.get(base_url, timeout=10).text
    except RequestException as e:
        print(f"Error fetching base URL: {e}")
        return []

    soup = BeautifulSoup(html, 'html.parser')

    # Find all page links
    page_links = soup.find_all('a', class_='pagenumberer-item pagenumberer-item-link')
    print(f"Total pages: {last_page}")
    urls = []
    games_data = []
    count = 0

    # Collect game URLs from each page
    for i in range(1, last_page):  # Iterate through all pages
        if i == 1:
            url = base_url
        else:
            url = f'{base_url}?page={i}'

        try:
            html = requests.get(url, timeout=10).text
        except RequestException as e:
            print(f"Error fetching page {i}: {e}")
            continue

        soup = BeautifulSoup(html, 'html.parser')
        game_links = soup.find_all('a', class_='products-view-name-link')

        # Добавление URL игр в список
        for link in game_links:
            game_url = link.get('href')
            urls.append(game_url)
            count += 1

    print(f"Total game URLs collected: {len(urls)}")

    # Получение страницы и её данных по ссылке
    for url in urls:
        try:
            html = requests.get(url, timeout=10).text
        except RequestException as e:
            print(f"Error fetching game URL {url}: {e}")
            continue

        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('h1', itemprop='name')
        photo_url_tag = soup.find('img', class_='gallery-picture-obj')
        price_tag = soup.find('div', class_='price-number')
        try:
            html = requests.get(url + "?tab=tabDescription", timeout=10).text
        except RequestException as e:
            print(f"Error fetching description for {url}: {e}")
            continue

        soup = BeautifulSoup(html, 'html.parser')
        description_tag = soup.find('div', class_='tab-content details-tabs-deacription clear')

        try:
            html = requests.get(url + "?tab=tabOptions", timeout=10).text
        except RequestException as e:
            print(f"Error fetching options for {url}: {e}")
            continue

        soup = BeautifulSoup(html, 'html.parser')
        age_tag = soup.find('li', class_='properties-item properties-item-even')

        if title_tag:
            title = title_tag.text.strip().replace("Настольная игра", "").strip()
            title = re.sub(
                r'\s*\((?=.*?(2-е\.?\s*рус\.?\s*изд|3-е\.?\s*рус\.?\s*изд|2021|2020|2019|2018|2017|2016|2015|2014|2013|2012|2011)).*?\)',
                '', title,
                flags=re.IGNORECASE)
            title = re.sub(r'\s*арт\.\s*\d+', '', title).strip()
            title = title.replace(" : ", " ").strip()
            title = title.capitalize()
            if title == ": манчкин 2. дикий топор,":
                title = "Манчкин 2 дикий топор"

        else:
            title = "Название не найдено"

        if description_tag:
            description = description_tag.get_text(separator='\n').strip().replace('\n', ' ')
            description = description.lstrip(' ')
        else:
            description = "Описание не найдено"

        if photo_url_tag:
            photo_url = photo_url_tag.get('src')
        else:
            photo_url = "Изображение не найдено"

        if price_tag:
            price = price_tag.get_text().replace(" ", "").strip()
        else:
            price = "Цена не найдена"

        if age_tag:
            age = age_tag.get_text().replace("\n", " ").strip().replace("Возраст", "").strip()
            age = age.split(', ')
            if len(age) >= 2:
                age = str(age[0] + "+")
            else:
                age = age[-1] + "+"
        else:
            age = "Возраст не найден"

        product_data = {
            'Название': title,
            'Описание': description,
            'Цена': price,
            'Изображение': photo_url,
            'URL': url,
            'Возраст': age
        }
        games_data.append(product_data)
        print(product_data)
    return games_data

# games = scrape_games_data_goodork(2)
