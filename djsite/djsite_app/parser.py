from LxmlSoup import LxmlSoup
import requests

html = requests.get('https://goodork.ru/categories/nastolnye-igry').text #html код сайта
soup = LxmlSoup(html) #Объект LXML
count = 0
pages = soup.find_all('a', class_='pagenumberer-item pagenumberer-item-link')
pages_value = []
urls = []

for page in pages:
    pages_value = page.text()


for i in range(2):
    if i == 0 or i == 1:
        html = requests.get(f'https://goodork.ru/categories/nastolnye-igry').text
        soup = LxmlSoup(html)
        links = soup.find_all('a', class_='products-view-name-link')
        for link in links:
            url = link.get('href')
            urls.append(url)
    else:
        html = requests.get(f'https://goodork.ru/categories/nastolnye-igry?page={i}').text
        soup = LxmlSoup(html)
        links = soup.find_all('a', class_='products-view-name-link')
        for link in links:
            url = link.get('href')
            urls.append(url)

for url in urls:
    html = requests.get(url).text
    soup = LxmlSoup(html)
    title = soup.find_all('div', class_='details-title')
    print(title)
    # description
    # photo
    # category
    # price
    # vendor
    # year
    # number_of_players
    # age


