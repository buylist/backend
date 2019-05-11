from django.core.management.base import BaseCommand
from mainapp.models import Buyer, Category, Item
import os
import json

JSON_PATH = 'mainapp/json'


# Загружаем из json файлов данные в базу
def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):
        # Создаем суперпользователя и подгружаем из файла пользователей по умолчанию
        buyers = load_from_json('buyers')

        Buyer.objects.all().delete()

        # Создаем суперпользователя при помощи менеджера модели
        _superuser = Buyer.objects.filter(username='admin').first()
        if not _superuser:
            Buyer.objects.create_superuser('admin', 'buylist.project@gmail.com', 'y1u2i3o4y1u2i3o4')
            print('SU created')

        buyers_objs = []
        for buyer in buyers:
            buyers_objs.append(Buyer(**buyer))

        Buyer.objects.bulk_create(buyers_objs)
        print('Тестовые пользователи подгружены!')

        # Подгружаем категории товара из списка
        categories = load_from_json('categories')

        Category.objects.all().delete()

        category_objs = []
        for category in categories:
            buyer_name = category['buyer']

            # Получаем пользователя "создавшего" категорию по имени
            _buyer = Buyer.objects.filter(username=buyer_name).first()

            # Заменяем имя пользователя идентификатором из базы
            category['buyer'] = _buyer
            category_objs.append(Category(**category))

        Category.objects.bulk_create(category_objs)
        print('Каталоги товаров подгружены!')

        # Подгружаем список товаров из списка
        items = load_from_json('items')

        Item.objects.all().delete()

        # Так как я не понял зачем нам item_id и с чем он должен связываться, решил генерить его по порядку с нуля
        item_id = 0

        item_objs = []
        for item in items:
            buyer_name = item['buyer']
            category_name = item['category']

            # Получаем пользователя "создавшего" категорию и саму категорию по именам
            _buyer = Buyer.objects.filter(username=buyer_name).first()
            _category = Category.objects.filter(name=category_name).first()

            # Заменяем имя пользователя и название категории идентификаторами из базы
            item['buyer'] = _buyer
            item['category'] = _category
            item['item_id'] = item_id

            item_objs.append(Item(**item))
            item_id = item_id + 1

        Item.objects.bulk_create(item_objs)
        print('Товары подгружены!')
        print('Заполнение базы завершено!')