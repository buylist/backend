import requests
import pprint
import datetime

TEST_TOKEN = 'Token cac73d18bb17caee51d96aff38bdb2eb5d476836'
PROD_TOKEN = 'Token 58899e03b06a48d09e21bc3f239fca652a8b2de1'

TEST_URL = '127.0.0.1:8000'
PROD_URL = '35.228.148.217:80'

user_local = {"username": "buylist.project+1@gmail.com", "password": "testy1u2i3o4"}


def test_auth():
    url = 'http://35.228.148.217:8000/api/token/'
    r = requests.post(url, data={"username": "by2@list.ru", "password": "123"})
    return r.json()


# print(test_auth())
'''
{'token': '367fd78a2c51efa9c047f27121845bd90e7e5f88'}
'''


# Запрос на получения токена
def get_token():
    url = f'http://{PROD_URL}/api/token/'
    r = requests.post(url, data=user_local)
    print(r.headers)
    return r.json()


# print(get_token())
'''
{'token': '80029d4e0d7ed1833a605e00c1335db9472ef5ff'}
'''


def share_list():
    url = f'http://{TEST_URL}/api/checklists/share/'
    r = requests.post(url, headers={"Authorization": TEST_TOKEN}, json={"mobile_id": 100})
    print(r.headers)
    return r.json()


# print(share_list())


def noshare_list():
    url = f'http://{TEST_URL}/api/checklists/noshare/'
    r = requests.post(url, headers={"Authorization": TEST_TOKEN}, json={"mobile_id": 100})
    print(r.headers)
    return r.json()


# print(noshare_list())


def save_shared_to_origin():
    url = f'http://{TEST_URL}/api/checklists/pull_to_origin/'
    r = requests.post(url, headers={"Authorization": TEST_TOKEN}, json={"mobile_id": 100})
    print(r.headers)
    return r.json()


# print(save_shared_to_origin())


def get_users():
    url = 'http://127.0.0.1:8000/api/v1/users/'
    r = requests.get(url, headers={"Authorization": "Token 80029d4e0d7ed1833a605e00c1335db9472ef5ff"})
    return r.json()


# pprint.pprint(get_users())
'''

'''


def get_categories():
    url = 'http://35.228.148.217:8000/api/v1/categories/'
    r = requests.get(url, headers={"Authorization": "Token 9c65603928b743c64480e88dea77a50fd90f3f41"})
    return r.json()


# pprint.pprint(get_categories())
#
'''

'''


def add_category():
    url = 'http://35.228.148.217:8000/api/v1/categories/'
    r = requests.post(url, headers={"Authorization": "Token 9c65603928b743c64480e88dea77a50fd90f3f41"}, json={
        'name': 'Овощи',
        'color': 'green'
    })
    print(r)
    return r.json()


# pprint.pprint(add_category())
'''

'''


def update_category():
    url = f'http://{TEST_URL}/api/v1/categories/12/'
    r = requests.patch(url, headers={"Authorization": TEST_TOKEN}, json={
        'name': 'СпортПИТ',
        'color': 'blue',
    })
    print(r)
    return r.json()


# pprint.pprint(update_category())

'''
{'color': 'red',
 'modified': '2019-05-28T05:45:34.876276Z',
 'name': 'Какашан',
 'url': 'http://127.0.0.1:8000/api/v1/categories/3/'}
'''


def delete_category():
    url = 'http://127.0.0.1:8000/api/v1/categories/20/'
    r = requests.delete(url, headers={"Authorization": "Token 80029d4e0d7ed1833a605e00c1335db9472ef5ff"})
    print(r)
    return r.status_code


# pprint.pprint(delete_category())
'''
<Response [204]>
'''


def get_lists():
    url = f'http://{TEST_URL}/api/v1/lists/'
    r = requests.get(url, headers={"Authorization": TEST_TOKEN})
    return r.json()


# pprint.pprint(get_lists())
'''

'''


def add_list():
    url = f'http://{PROD_URL}/api/v1/lists/'
    r = requests.post(url, headers={"Authorization": PROD_TOKEN}, json={
        'name': 'день рождения',
        'mobile_id': 100,
        'items': [
            {
                "item": {"name": "Картофель", "category": "Овощи и фрукты", 'mob_cat_id': 0, "mobile_id": 0},
                "unit": "кг",
                "quantity": 5,
                "deleted": "False",
            },
            {
                "item": {"name": "Орешки", "category": "Снэки", 'mob_cat_id': 0, "mobile_id": 100},
                "unit": "кг",
                "quantity": 1,
                "deleted": "False",
            },
            {
                "item": {"name": "Сухарики", "category": "Снэки", 'mob_cat_id': 0, "mobile_id": 101},
                "unit": "гр",
                "quantity": 500,
                "deleted": "False",
            },
            {
                "item": {"name": "Чипсы", "category": "Снэки", 'mob_cat_id': 0, "mobile_id": 102},
                "unit": "гр",
                "quantity": 2,
                "deleted": "False",
            },
        ]

    })
    print(f' add_list(): {r}')
    print(f"headers {r.headers}")
    return r.json()


# pprint.pprint(add_list())
'''

'''


def update_list():
    url = f'http://{TEST_URL}/api/v1/lists/1/'
    r = requests.patch(url, headers={"Authorization": TEST_TOKEN}, json={
        'name': 'ДеньВаренья',
        'mobile_id': 100,
        'items': [
            {
                "item": {"name": "Сухарики", "category": "Снэки", 'mob_cat_id': 0, "mobile_id": 101},
                "unit": "шт",
                "quantity": 20,
                "deleted": "False",
            },
            {
                "item": {"name": "Чипсы", "category": "Снэки", 'mob_cat_id': 0, "mobile_id": 102},
                "unit": "шт",
                "quantity": 2,
                "deleted": "True",
            },
        ]
    })
    print(f' update_list(): {r}')
    print(f"headers {r.headers}")
    return r.json()


# pprint.pprint(update_list())
'''

'''


def delete_list():
    url = f'http://{TEST_URL}/api/v1/lists/1/'
    r = requests.delete(url, headers={"Authorization": TEST_TOKEN})
    print(r)
    return r.status_code


# pprint.pprint(delete_list())
'''
<Response [204]>
'''


def get_items():
    url = f'http://{TEST_URL}/api/v1/items/'
    r = requests.get(url, headers={"Authorization": TEST_TOKEN})
    return r.json()


# pprint.pprint(get_items())

'''

'''


def add_items():
    url = f'http://{TEST_URL}/api/v1/items/'
    r = requests.post(url, headers={"Authorization": TEST_TOKEN}, json={
        'name': 'Cola',
        'category': 'СпортПИТ',
        'mob_cat_id': 21,
        'mobile_id': 653,
    })
    print(r)
    return r.json()


# pprint.pprint(add_items())

'''

'''


# Можно указывать тока те поля в запросе которые собираемся поменять
def update_item():
    url = f'http://{TEST_URL}/api/v1/items/47/'
    r = requests.patch(url, headers={"Authorization": TEST_TOKEN}, json={
        'name': 'Coca-Cola',
        'category': 'Газировка',
        'mob_cat_id': 21,
    })
    print(r)
    return r.json()


# pprint.pprint(update_item())
'''

'''

def delete_item():
    url = 'http://35.228.148.217:8000/api/v1/items/2/'
    r = requests.delete(url, headers={"Authorization": "Token 9c65603928b743c64480e88dea77a50fd90f3f41"})
    print(r)
    return r.status_code


# pprint.pprint(delete_item())
'''
<Response [204]>
'''

# checklist must already exist in db or will responce 400 or error Nonobject doesn't have "id"
def add_item_in_checklist():
    url = f'http://{TEST_URL}/api/v1/checklists/'
    r = requests.post(url, headers={"Authorization": TEST_TOKEN}, json={
        'mob_item_id': 35,
        'item_name': 'Корица',
        'checklist_name': 'ДеньВаренья',
        'mob_check_id': 100,
        'deleted': "False",
        'quantity': 8,
        'unit': 'шт'
    })
    print(r)
    for h in r.headers.items():
        print(h)
    return r.json()


# pprint.pprint(add_item_in_checklist())
'''

'''


def update_item_in_checklist():
    url = f'http://{TEST_URL}/api/v1/checklists/6/'
    r = requests.patch(url, headers={"Authorization": TEST_TOKEN}, json={
        'deleted': 'True',
        'quantity': 6,
    })
    print(r)
    return r.json()


# pprint.pprint(update_item_in_checklist())
'''

'''


def delete_item_from_list():
    url = f'http://{TEST_URL}/api/v1/checklists/2/'
    r = requests.delete(url, headers={"Authorization": TEST_TOKEN})
    print(r)
    return r.status_code


# pprint.pprint(delete_item_from_list())
'''
<Response [204]>
'''


def get_reciept():
    url = f'http://{TEST_URL}/api/v1/reciept/'
    r = requests.get(url, headers={"Authorization": TEST_TOKEN})
    print(r)
    return r.json()


# pprint.pprint(get_reciept())


def add_reciept():
    """
    <Response [201]>
    {'name': 'Test_pattern', 'url': 'http://127.0.0.1:8000/api/v1/pattern/1/'}
    """
    url = f'http://{TEST_URL}/api/v1/reciept/'
    r = requests.post(url, headers={"Authorization": TEST_TOKEN}, json={
        'name': 'Test_reciept',
        'mobile_id': 1445517,
        'description': 'Это рецепт борща'
    })
    print(r)
    return r.json()

# pprint.pprint(add_reciept())


def add_item_in_reciept():
    url = f'http://{TEST_URL}/api/v1/reciept_item/'
    r = requests.post(url, headers={"Authorization": "Token 80029d4e0d7ed1833a605e00c1335db9472ef5ff"}, json={
        'item': 'Orange',
        'reciept': 'Test_reciept',
        'deleted': False,
        'quantity': 3,
        'unit': 'шт'
    })
    print(r)
    return r.json()
# pprint.pprint(add_item_in_reciept())


def update_item_in_reciept():
    url = 'http://127.0.0.1:8000/api/v1/reciept_item/3/'
    r = requests.patch(url, headers={"Authorization": TEST_TOKEN}, json={
        'deleted': True,
    })
    print(r)
    return r.json()
# pprint.pprint(update_item_in_reciept())


def delete_item_from_reciept():
    url = 'http://127.0.0.1:8000/api/v1/reciept_item/3/'
    r = requests.delete(url, headers={"Authorization": TEST_TOKEN})
    print(r)
    return r.status_code

# pprint.pprint(delete_item_from_reciept())