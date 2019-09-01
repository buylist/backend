import requests
import re
from functools import reduce
from decimal import Decimal, getcontext

getcontext().prec = 8


def trans_measure(to_unit, splited_vol):
    res = splited_vol['quantity']
    to_unit = to_unit.lower()
    list_of_measures = {
        'г': {'кг': Decimal(0.001), 'гр': Decimal(1)},
        'гр': {'кг': Decimal(0.001), 'г': Decimal(1)},
        'кг': {'г': Decimal(1000), 'гр': Decimal(1000)},
        'мл': {'л': Decimal(0.001)},
        'л': {'мл': Decimal(1000)},
        'уп': {},
        'шт': {},
    }

    gage = list_of_measures.get(to_unit, None)

    if gage:
        if splited_vol['measure'] == to_unit:
            pass
        elif gage.get(splited_vol['measure'], None):
            res /= gage[splited_vol['measure']]
        else:
            print(f'{to_unit} нельзя привести к {splited_vol["measure"]}')
            res = 0

    return res


def split_volume(volume, measure_reg_expr='[гкштуплмГКШТУПЛМ]{1,2}'):
    try:
        quantity, measure = re.findall(r'[0-9]{1,6}|'+measure_reg_expr, volume)

        res = {
            'quantity': Decimal(quantity),
            'measure': measure
        }
    except ValueError:

        res = volume

    return res


def transform_str_to_decimals(str_obj):
    if ',' in str_obj:
        str_obj = str_obj.split(',')
        str_obj = Decimal(reduce(lambda x, y: str(x) + '.' + str(y), str_obj))
    return str_obj


def find_fields(product, prod_fields, available_list_of_fields, reg_expr, marker=' UUU ', semantic_distance=10):
    prod = product.lower()
    marker = marker.lower()
    marker = marker.lstrip()
    marker = marker.rstrip()

    prod_name_parts = prod.split(' ')

    vers_of_splited_pn = [
        prod_name_parts,
    ]

    ind = 0
    partially_match = False

    end = len(available_list_of_fields)

    res = {}
    sec_res = {}

    full_match_keys = []
    partly_match_keys = []
    t = 0

    while not ind and t < len(vers_of_splited_pn):
        start = 0
        while vers_of_splited_pn[t][0] in available_list_of_fields[start:end]:
            res_ind = available_list_of_fields[start:end].index(vers_of_splited_pn[t][0]) + start

            if available_list_of_fields[res_ind - 1] == marker:
                full_match_possibility = True
            else:
                full_match_possibility = False

            i = 0

            try:
                while vers_of_splited_pn[t][0 + i] == available_list_of_fields[res_ind + i]:
                    i += 1
                else:
                    start = res_ind + i
                    ind = None

            except IndexError:
                if (not re.match(r'' + reg_expr['prod_name'], available_list_of_fields[res_ind + i]) or
                    available_list_of_fields[res_ind + i] == marker) and \
                        full_match_possibility:

                    ind = res_ind

                    temp_name = 'PROD_'+str(t)+'_'+str(res_ind+i-1)
                    full_match_keys.append((temp_name, ind))

                    print(f'GOT FULL MATCH: VER_product {vers_of_splited_pn[t]}')

                    res[temp_name] = {}

                    res[temp_name]['prod_name'] = prod
                    res[temp_name]['web_prod_name'] = reduce(lambda x, y: x + ' ' + y, vers_of_splited_pn[t])

                    start = res_ind + i
                else:
                    temp_name = 'prod_partly_'+str(t)+'_'+str(res_ind+i-1)
                    partly_match_keys.append((temp_name, res_ind))

                    sec_res[temp_name] = {}

                    sec_res[temp_name]['prod_name'] = prod
                    sec_res[temp_name]['web_prod_name'] = ''

                    o = 0
                    try:
                        while re.match(r'' + reg_expr['prod_name'], available_list_of_fields[res_ind + o]) and \
                                available_list_of_fields[res_ind + o] != marker:
                            sec_res[temp_name]['web_prod_name'] += ' ' + available_list_of_fields[res_ind + o]
                            o += 1
                    except IndexError:
                        pass

                    sec_res[temp_name]['web_prod_name'] = sec_res[temp_name]['web_prod_name'][1:]

                    ind = None
                    partially_match = True
                    start = res_ind + i

        t += 1

    if len(full_match_keys) > 0:
        for prod_n, prod_i in full_match_keys:
            for prod_f in prod_fields:
                correction_for_marker = 0
                for i, field_form_web in enumerate(available_list_of_fields[prod_i:]):
                    if field_form_web == marker:
                        correction_for_marker += 1

                    if re.match(r''+reg_expr[prod_f], field_form_web):
                        if i < semantic_distance + correction_for_marker:
                            if prod_f == 'price':
                                res[prod_n][prod_f] = transform_str_to_decimals(field_form_web)
                            else:
                                res[prod_n][prod_f] = field_form_web
                        break
                    else:
                        if prod_f == 'volume' and res[prod_n]['measure']:
                            res[prod_n][prod_f] = '1' + res[prod_n]['measure']
                        else:
                            res[prod_n][prod_f] = ''
    else:
        if partially_match:
            sec_res['NO_FULL_MATCH'] = 'TOO_WIDE_MAPPING. GOT ONLY PARTIALLY MATCH. SPECIFY_PROD_NAME'
        else:
            sec_res['NO_FULL_MATCH'] = 'NO_MATCH_AT_ALL'

        for prod_n, prod_i in partly_match_keys:
            for prod_f in prod_fields:
                correction_for_marker = 0
                for i, field_form_web in enumerate(available_list_of_fields[prod_i:]):
                    if field_form_web == marker:
                        correction_for_marker += 1

                    if re.match(r''+reg_expr[prod_f], field_form_web):
                        if i < semantic_distance + correction_for_marker:
                            if prod_f == 'price':
                                sec_res[prod_n][prod_f] = transform_str_to_decimals(field_form_web)
                            else:
                                sec_res[prod_n][prod_f] = field_form_web
                        break
                    else:
                        if prod_f == 'volume' and sec_res[prod_n]['measure']:
                            sec_res[prod_n][prod_f] = '1' + sec_res[prod_n]['measure']
                        else:
                            sec_res[prod_n][prod_f] = ''

        res = sec_res

    return res


def del_tag_content(text, open='<', close='>', mark=None, marker=' UUU '):
    open_tag = False
    close_tag = True

    res = ''

    for i, letter in enumerate(text):
        if letter == open:
            open_tag = True
            close_tag = False
        if letter == close:
            close_tag = True
            open_tag = False

        if open_tag and not close_tag:
            pass
        else:
            if letter == open:
                pass
            elif letter == close:
                if mark:
                    res += marker
                pass
            else:
                if letter == '.' or letter == ',':
                    while res.rfind(marker) + len(marker) == len(res):
                        res = res[:-len(marker)]

                res += str(letter)

    return res


class Parser:
    def __init__(self, products, web_config):
        self.products = list(set(products))
        self.prod_fields = []
        self.web_config = web_config
        self.dict = {}
        self.list_of_res = []

    def extract_from_www(self):
        for www in self.web_config:
            self.prod_fields = list(www['reg_expr'].keys())
            self.prod_fields.remove('prod_name')
            self.dict[www['adr']] = {}

            for prod in self.products:
                url_param = str(www['search_exp'])+str(prod)
                info = requests.get(www['adr'], params=url_param)
                clear_data = del_tag_content(info.text, mark=True)
                clear_data = del_tag_content(clear_data, open='[', close=']')
                clear_data = re.findall(r''+www['reg_expr']['measure']+'|'
                                        + www['reg_expr']['volume'] + '|'
                                        + www['reg_expr']['price']+'|'
                                        + www['reg_expr']['prod_name'], clear_data)

                clear_data = [i.lower() for i in clear_data]

                self.dict[www['adr']][prod] = []

                found = find_fields(prod, self.prod_fields, clear_data, www['reg_expr'],
                                    semantic_distance=www['semantic_dist'])

                if 'NO_FULL_MATCH' not in found:
                    found = found.values()
                    for f_prod in found:
                        if f_prod[self.prod_fields[0]]:
                            f_prod['source'] = www['adr']
                            self.dict[www['adr']][prod].append(f_prod)
                else:
                    found = found.values()
                    for f_prod in found:
                        if type(f_prod) != str and f_prod[self.prod_fields[0]]:
                            f_prod['source'] = www['adr']
                            self.dict[www['adr']][prod].append(f_prod)

            temp_res = list(self.dict[www['adr']].values())

            for list_of_res in temp_res:
                for res in list_of_res:
                    if res not in self.list_of_res:
                        self.list_of_res.append(res)
                        print(res)

    def django_models_into_db(self, class_model):
        model_objects_list = []
        existing_objects = class_model.objects.all()

        print(f'Всего объектов в {class_model} до обновления {len(existing_objects)}')

        for res in self.list_of_res:
            model_objects_list.append(class_model(**res))

        existing_objects.delete()
        class_model.objects.bulk_create(model_objects_list)

        print(f'Всего объектов в {class_model} после обновления {len(class_model.objects.all())}')

    @classmethod
    def django_value_field_update(cls, from_model, objects_to_update):
        for obj in objects_to_update:
            # идентифицируем по полю name
            attr = obj.item.name
            attr = attr.lower()
            source_objects = from_model.objects.filter(prod_name=attr).order_by('price')

            apropriate_values = []

            for source_obj in source_objects:
                # func separates volume format 400гр то {quantity: 400, measure: гр}
                splited_vol = split_volume(source_obj.volume)
                # func leads to common denomination, ex.: 1кг to 1000гр
                estimated_quantity = trans_measure(obj.unit, splited_vol)

                if obj.quantity:
                    if obj.unit and estimated_quantity:
                        apropriate_values.append((obj.quantity/estimated_quantity) * source_obj.price)
                    else:
                        apropriate_values.append(obj.quantity * source_obj.price)
                else:
                    apropriate_values.append(source_obj.price)

            try:
                setattr(obj, 'value', min(apropriate_values))
                obj.save()
            except ValueError:
                print(f'CANNOT ESTIMATE VALUE FOE item.name {obj.item.name}: NO SOURCE IN FromWebProdFields')

    @classmethod
    def django_models_clear_db(cls, class_model):
        class_model.objects.all().delete()

    @classmethod
    def django_models_show_db(cls, class_model):
        objects = class_model.objects.all()
        for obj in objects:
            atrr_list = []
            for atrr, _ in obj.__dict__.items():
                atrr_list.append(getattr(obj, atrr))
            atrr_list = atrr_list[2:]
            print(*atrr_list)


if __name__ == '__main__':
    products = ['картофель']

    web_config = [
        {
            'adr': 'https://www.perekrestok.ru/catalog/search',
            'search_exp': 'text=',
            'semantic_dist': 10,
            'reg_expr': {
                'price': '[0-9]{1,5}[,.]{1}[0-9]{2}[рубРУБRURrur]{0,3}',
                'measure': '^[гкштуплмГКШТУПЛМ]{1,2}$',
                'volume': '[0-9]{1,4}[гкштуплмГКШТУПЛМ]{1,2}',
                'prod_name': '[А-Яа-яA-Za-z]+'
            }
        }
    ]

    parser = Parser(products=products, web_config=web_config)
    parser.extract_from_www()
