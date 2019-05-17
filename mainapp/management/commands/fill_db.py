from django.core.management.base import BaseCommand
from mainapp.models import Buyer, Category, Item
from django.conf import settings
import os
import json


# Загружаем из json файлов данные в базу
def load_from_json(file_name):
    with open(os.path.join(settings.BASE_DIR, 'mainapp', 'json', file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):
        # Подгружаем из файлов суперпользователей (su) и пользователей (buyer)
        superuser = load_from_json('su')
        buyers = load_from_json('buyers')

        Buyer.objects.all().delete()

        # Создаем суперпользователей
        for su in superuser:
            Buyer.objects.create_superuser(**su)
        print('SU created')

        # Создаем пользователей
        for buyer in buyers:
            Buyer.objects.create_user(**buyer)
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
