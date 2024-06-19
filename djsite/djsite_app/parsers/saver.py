import os
import django
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException

from djsite_app.parsers.parser_of_igroved import scrape_games_data_igroved
from djsite_app.parsers.parser_of_lavka_orka import scrape_games_data_goodork

# Установка переменной окружения для настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsite.settings")
django.setup()

from djsite_app.models import Game


def save_games_to_database(games_data):
    for game_data in games_data:
        # Создаем запись, если нет "названия". Если название имеется - получаем запись
        game, created = Game.objects.get_or_create(
            title=game_data['Название'],
            defaults={
                'url': game_data['URL'],
                'description': game_data['Описание'],
                'photo': game_data['Изображение'],
                'price': int(game_data['Цена']) if game_data['Цена'].isdigit() else 0,
                'age': game_data['Возраст'],
                'vendor': game_data.get('Производитель', ''),
                'number_of_players': game_data.get('Количество игроков', '')
            }
        )

        # Если запись не была создана, то смотрим на налиличие данных в записе и добавляем
        if not created:
            fields_to_update = False
            if not game.url and game_data['URL']:
                game.url = game_data['URL']
                fields_to_update = True
            if not game.description and game_data['Описание']:
                game.description = game_data['Описание']
                fields_to_update = True
            if not game.photo and game_data['Изображение']:
                game.photo = game_data['Изображение']
                fields_to_update = True
            if not game.price and game_data['Цена'].isdigit():
                game.price = int(game_data['Цена'])
                fields_to_update = True
            if not game.age and game_data['Возраст']:
                game.age = game_data['Возраст']
                fields_to_update = True
            if not game.vendor and game_data.get('Производитель'):
                game.vendor = game_data['Производитель']
                fields_to_update = True
            if not game.number_of_players and game_data.get('Количество игроков'):
                game.number_of_players = game_data['Количество игроков']
                fields_to_update = True

            if fields_to_update:
                game.save()
                print(f"Updated game: {game}")
            else:
                print(f"No updates needed for game: {game}")

        # В противном случае просто делаем новую запись
        else:
            print(f"Saved new game: {game}")


# Объявление функций
games_igroved = scrape_games_data_igroved(2)
games_godork = scrape_games_data_goodork(2)

# Сохранение
save_games_to_database(games_igroved)
save_games_to_database(games_godork)

print(f"Total games scraped: {len(games_igroved)+len(games_godork)}")