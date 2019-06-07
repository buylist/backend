from django.core.management.base import BaseCommand
from mainapp.models import Item as Product, FromWebProdFields, ItemInChecklist, Checklist, Category
from mainapp.parser.parser import Parser
import json
import sys


confiq_address = 'mainapp/parser/configures.json'


class Command(BaseCommand):
    help = 'Run parser which collect data from web-sites and add it to the database'

    def add_arguments(self, parser):
        parser.add_argument('-clear_db', action='store_true', default=False, help='clears tab FromWebProdFields in db')
        parser.add_argument('--show_db', type=str, action='store', default=False, help='shows selected tab in db')

    def handle(self, *args, **options):
        if options['clear_db']:

            Parser.django_models_clear_db(FromWebProdFields)
            print('CLEAR DB IS DONE')

        elif options['show_db']:
            model = getattr(sys.modules[__name__], options['show_db'], 'NO SUCH MODEL ')
            if model == 'NO SUCH MODEL ':
                print(model + options['show_db'])
            else:
                Parser.django_models_show_db(model)

        else:
            prod_names = Product.objects.values_list('name', flat=True)
            prod_names = list(set(prod_names))

            with open(confiq_address, 'r', encoding='utf-8') as infile:
                web_confiq = json.load(infile)

            data = Parser(prod_names, web_confiq)
            data.extract_from_www()
            data.django_models_into_db(FromWebProdFields)

            check_lists = ItemInChecklist.objects.all()

            Parser.django_value_field_update(FromWebProdFields, check_lists)