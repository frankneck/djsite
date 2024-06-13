import re, os, django
from bs4 import BeautifulSoup
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsite.settings")
django.setup()

from djsite_app.models import Game


def scrape_games_data():
    base_url = 'https://goodork.ru/categories/nastolnye-igry'
    html = requests.get(base_url).text
    soup = BeautifulSoup(html, 'html.parser')

    # Find all page links
    page_links = soup.find_all('a', class_='pagenumberer-item pagenumberer-item-link')
    page_values = [link.text for link in page_links][-1]
    print(page_values)
    urls = []
    games_data = []

    # Collect game URLs from each page
    for i in range(len(page_values)):  # Iterate through all pages
        if i == 0:
            url = base_url
        else:
            url = f'{base_url}?page={i}'

        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        game_links = soup.find_all('a', class_='products-view-name-link')

        for link in game_links:
            game_url = link.get('href')
            urls.append(game_url)


    # Scrape data for each game
    for url in urls:
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        title_tag = soup.find('h1', itemprop='name')
        photo_url_tag = soup.find('img', class_='gallery-picture-obj')
        price_tag = soup.find('div', class_='price-number')

        html = requests.get(url + "?tab=tabDescription").text
        soup = BeautifulSoup(html, 'html.parser')
        description_tag = soup.find('div', class_='tab-content details-tabs-deacription clear')

        html = requests.get(url + "?tab=tabOptions").text
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

    return games_data


def save_games_to_database(games_data):
    for game_data in games_data:
        game = Game.objects.create(
            title=game_data['Название'],
            description=game_data['Описание'],
            photo=game_data['Изображение'],
            price=int(game_data['Цена']),
            age=game_data['Возраст']
        )
        game.save()


games = scrape_games_data()
save_games_to_database(games)

for i in range(len(games)):
    print(games[i])
print("Total games scraped:", len(games))
