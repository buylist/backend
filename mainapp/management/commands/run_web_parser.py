from django.core.management.base import BaseCommand
from mainapp.models import Item as Product, FromWebProdFields, ItemInChecklist, Checklist, Category
from mainapp.parser.parser import Parser
import json
import time
import sys


confiq_address = 'mainapp/parser/configures.json'


class Command(BaseCommand):
    help = 'Run parser which collect data from web-sites and add it to the database'

    def add_arguments(self, parser):
        parser.add_argument('--sleep', type=int, default=24,
                            action='store', help='make interval of sessions in hours')
        parser.add_argument('-clear_db', action='store_true', default=False, help='clears tab FromWebProdFields in db')
        parser.add_argument('--show_db', type=str, action='store', default=False, help='shows selected tab in db')

    def handle(self, *args, **options):
        sleep_interval = options['sleep']*60*60

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
            while True:
                products = Product.objects.all()
                prod_names = []
                for prod in products:
                    if prod not in prod_names:
                        prod_names.append(prod.name)

                with open(confiq_address, 'r', encoding='utf-8') as infile:
                    web_confiq = json.load(infile)

                data = Parser(prod_names, web_confiq)
                data.extract_from_www()
                data.django_models_into_db(FromWebProdFields)

                check_lists = ItemInChecklist.objects.all()

                Parser.django_value_field_update(FromWebProdFields, check_lists)

                print(f"i'm going sleep for {int(sleep_interval/3600)} hour(s)")

                elapsed_time = 0

                while elapsed_time < sleep_interval:
                    time.sleep(3600)
                    elapsed_time += 3600
