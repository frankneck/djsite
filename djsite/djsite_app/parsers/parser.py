import re
from bs4 import BeautifulSoup
import requests


def scrape_games_data():
    base_url = 'https://goodork.ru/categories/nastolnye-igry'
    html = requests.get(base_url).text
    soup = BeautifulSoup(html, 'html.parser')

    # Find all page links
    page_links = soup.find_all('a', class_='pagenumberer-item pagenumberer-item-link')
    page_values = [link.text for link in page_links]
    urls = []

    # Collect game URLs from each page
    for i in range(1):  # Iterate through all pages
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

    games_data = []

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
            title = re.sub(r'\s*\((?=.*?(2-е\.?\s*рус\.?\s*изд|3-е\.?\s*рус\.?\s*изд|2021)).*?\)', '', title,
                           flags=re.IGNORECASE)
            title = re.sub(r'\s*арт\.\s*\d+', '', title).strip()
            title = title.replace(" : ", " ").strip()
            title = title.capitalize()

        else:
            title = "Title not found"

        if description_tag:
            description = description_tag.get_text(separator='\n').strip().replace('\n', ' ')
            description = description.lstrip(' ')
        else:
            description = "Description not found"

        if photo_url_tag:
            photo_url = photo_url_tag.get('src')
        else:
            photo_url = "Photo URL not found"

        if price_tag:
            price = price_tag.get_text().strip()
        else:
            price = "Price not found"

        if age_tag:
            age = age_tag.get_text().replace("\n", " ").strip().replace("Возраст", "").strip()
            age = age.split(', ')
            if len(age) >= 2:
                age = str(age[0] + " - " + age[-1])
            else:
                age = age[-1]
        else:
            age = "Age not found"

        # Print or store data
        print("Age:", age)
        print("Price:", price)
        print("Image:", photo_url)
        print("Title:", title)
        print("Description:", description, "\n")

        # Store data in dictionary
        product_data = {
            'title': title,
            'description': description,
            'price': price,
            'image': photo_url,
            'url': url,
            'age': age
        }
        games_data.append(product_data)

    return games_data


# Example usage:
games = scrape_games_data()
print("Total games scraped:", len(games))
