from .models import *
from LxmlSoup import LxmlSoup
import requests

html = requests.get('https://goodork.ru/categories/nastolnye-igry').text #html код сайта
soup = LxmlSoup(html) #Объект LXML

links = soup.find_all('a', class_='products-view-name-link') #Список строк класса

collections_titles = []
collections_urls = []
collections_prices = []

for i, link in enumerate(links):
    url = link.get('href')
    title = soup.find_all('div', class_='products-view-name products-view-name-default')[i].text()
    price = soup.find_all('div',  class_='price-number')[i].text()
    print(f"URL: {url}")
    print(f"Title: {title}")
    print(f"Price: {price}")
    Game.title = title



