import requests
import pprint
import datetime

TEST_TOKEN = 'Token 80029d4e0d7ed1833a605e00c1335db9472ef5ff'
PROD_TOKEN = 'Token 9c65603928b743c64480e88dea77a50fd90f3f41'

TEST_URL = '127.0.0.1:8000'
PROD_URL = '35.228.148.217:8000'


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
    url = 'http://127.0.0.1:8000/api/token/'
    r = requests.post(url, data={"username": "123@mail.ru", "password": "123"})
    return r.json()


# print(get_token())
'''
{'token': '80029d4e0d7ed1833a605e00c1335db9472ef5ff'}
'''


def get_users():
    url = 'http://127.0.0.1:8000/api/v1/users/'
    r = requests.get(url, headers={"Authorization": "Token 80029d4e0d7ed1833a605e00c1335db9472ef5ff"})
    return r.json()


# pprint.pprint(get_users())
'''
[{'created': '2019-05-22T05:51:14.684923Z',
  'email': '123@mail.ru',
  'is_active': True,
  'modified': '2019-05-22T05:51:14.684935Z',
  'url': 'http://127.0.0.1:8000/api/v1/users/2/',
  'username': 'Serg'},
 {'created': '2019-05-21T18:29:25.838728Z',
  'email': '3481126@mail.ru',
  'is_active': True,
  'modified': '2019-05-21T18:29:25.844026Z',
  'url': 'http://127.0.0.1:8000/api/v1/users/1/',
  'username': 'Admin'}]
'''


def get_categories():
    url = 'http://35.228.148.217:8000/api/v1/categories/'
    r = requests.get(url, headers={"Authorization": "Token 9c65603928b743c64480e88dea77a50fd90f3f41"})
    return r.json()


# pprint.pprint(get_categories())
#
'''
[{'modified': '2019-05-22T13:40:01Z',
  'name': 'fruts',
  'url': 'http://127.0.0.1:8000/api/v1/categories/1/'},
 {'modified': '2019-05-22T13:40:01Z',
  'name': 'MustHave',
  'url': 'http://127.0.0.1:8000/api/v1/categories/2/'}]
'''


def add_category():
    url = 'http://35.228.148.217:8000/api/v1/categories/'
    r = requests.post(url, headers={"Authorization": "Token 9c65603928b743c64480e88dea77a50fd90f3f41"}, json={
        'name': 'Продукты',
        'color': 'green'
    })
    print(r)
    return r.json()


# pprint.pprint(add_category())
# '''
# <Response [201]>
'''
{'color': 'green',
 'modified': '2019-05-29T06:47:14.665436Z',
 'name': 'Мясо',
 'url': 'http://127.0.0.1:8000/api/v1/categories/10/'}
'''


def update_category():
    url = 'http://127.0.0.1:8000/api/v1/categories/20/'
    r = requests.patch(url, headers={"Authorization": "Token 80029d4e0d7ed1833a605e00c1335db9472ef5ff"}, json={
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
[{'items': [{'item': {'buyer_id': 2,
                      'category_id': 1,
                      'item_id': 1,
                      'name': 'Apple',
                      'url': 'http://127.0.0.1:8000/api/v1/items/1/'},
             'quantity': '2.0000',
             'unit': 'шт',
             'url': 'http://127.0.0.1:8000/api/v1/checklists/1/'},
            {'item': {'buyer_id': 2,
                      'category_id': 1,
                      'item_id': 2,
                      'name': 'Orange',
                      'url': 'http://127.0.0.1:8000/api/v1/items/2/'},
             'quantity': '3.0000',
             'unit': 'шт',
             'url': 'http://127.0.0.1:8000/api/v1/checklists/1/'}],
  'name': 'Lenta',
  'url': 'http://127.0.0.1:8000/api/v1/lists/1/'},
 {'items': [{'item': {'buyer_id': 2,
                      'category_id': 2,
                      'item_id': 3,
                      'name': 'Water',
                      'url': 'http://127.0.0.1:8000/api/v1/items/3/'},
             'quantity': '4.0000',
             'unit': 'шт',
             'url': 'http://127.0.0.1:8000/api/v1/checklists/2/'},
            {'item': {'buyer_id': 2,
                      'category_id': 1,
                      'item_id': 1,
                      'name': 'Apple',
                      'url': 'http://127.0.0.1:8000/api/v1/items/1/'},
             'quantity': '5.0000',
             'unit': 'шт',
             'url': 'http://127.0.0.1:8000/api/v1/checklists/2/'}],
  'name': 'EveryDay',
  'url': 'http://127.0.0.1:8000/api/v1/lists/2/'}]
'''


def add_list():
    url = 'http://35.228.148.217:8000/api/v1/lists/'
    r = requests.post(url, headers={"Authorization": "Token 9c65603928b743c64480e88dea77a50fd90f3f41"}, json={
        'name': 'ДР',
        'checklist_id': 117
    })
    print(r)
    return r.json()


# pprint.pprint(add_list())
'''
<Response [201]>
{'items': [],
 'name': 'день рождения',
 'url': 'http://127.0.0.1:8000/api/v1/lists/35/'}
'''


def update_list():
    url = 'http://127.0.0.1:8000/api/v1/lists/9/'
    r = requests.patch(url, headers={"Authorization": "Token 80029d4e0d7ed1833a605e00c1335db9472ef5ff"}, json={
        'name': 'Васьмая марта',
        'checklist_id': 112
    })
    print(r)
    return r.json()


# pprint.pprint(update_list())
'''
{'items': [], 'name': 'Овощи', 'url': 'http://127.0.0.1:8000/api/v1/lists/7/'}
'''


def delete_list():
    url = 'http://127.0.0.1:8000/api/v1/lists/9/'
    r = requests.delete(url, headers={"Authorization": "Token 80029d4e0d7ed1833a605e00c1335db9472ef5ff"})
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
[{'modified': '2019-05-22T13:40:01Z',
  'name': 'Apple',
  'url': 'http://127.0.0.1:8000/api/v1/items/1/'},
 {'modified': '2019-05-22T13:40:01Z',
  'name': 'Orange',
  'url': 'http://127.0.0.1:8000/api/v1/items/2/'},
 {'modified': '2019-05-22T13:40:01Z',
  'name': 'Water',
  'url': 'http://127.0.0.1:8000/api/v1/items/3/'}]
'''


def add_items():
    url = 'http://35.228.148.217:8000/api/v1/items/'
    r = requests.post(url, headers={"Authorization": "Token 9c65603928b743c64480e88dea77a50fd90f3f41"}, json={
        'name': 'Пельмеши',
        'category_name': 'Продукты',
        'item_id': 653
    })
    print(r)
    return r.json()


# pprint.pprint(add_items())

'''
{'category_id': 4,
 'item_id': 11,
 'name': 'KOLBOSA',
 'url': 'http://127.0.0.1:8000/api/v1/items/11/'}
'''


# Можно указывать тока те поля в запросе которые собираемся поменять
def update_item():
    url = 'http://35.228.148.217:8000/api/v1/items/2/'
    r = requests.patch(url, headers={"Authorization": "Token 9c65603928b743c64480e88dea77a50fd90f3f41"}, json={
        'name': 'Coca-Cola',
    })
    print(r)
    return r.json()


# pprint.pprint(update_item())
'''
{'buyer_id': 1,
 'category_id': 3,
 'item_id': 6,
 'name': 'Кофе',
 'url': 'http://127.0.0.1:8000/api/v1/items/6/'}
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


def add_item_in_checklist():
    url = f'http://{PROD_URL}/api/v1/checklists/'
    r = requests.post(url, headers={"Authorization": PROD_TOKEN}, json={
        'item': 'Пельмеши',
        'checklist': '8марта',
        'deleted': True,
        'quantity': 4,
        'unit': 'шт'
    })
    print(r)
    return r.json()


# pprint.pprint(add_item_in_checklist())
'''
<Response [201]>
{'checklist_id': 8,
 'delete': False,
 'item_id': 3,
 'modified': '2019-05-30T12:12:24.541094Z',
 'quantity': '8.0000',
 'unit': 'шт',
 'url': 'http://127.0.0.1:8000/api/v1/checklists/13/'}
'''


def update_item_in_checklist():
    url = 'http://127.0.0.1:8000/api/v1/checklists/21/'
    r = requests.patch(url, headers={"Authorization": TEST_TOKEN}, json={
        'deleted': False,
    })
    print(r)
    return r.json()


# pprint.pprint(update_item_in_checklist())
'''
{'checklist_id': 4,
 'delete': True,
 'item_id': 7,
 'modified': '2019-05-29T06:08:12.093432Z',
 'quantity': '9.0000',
 'unit': 'шт',
 'url': 'http://127.0.0.1:8000/api/v1/checklists/4/'}
'''


def delete_item_from_list():
    url = 'http://127.0.0.1:8000/api/v1/checklists/12/'
    r = requests.delete(url, headers={"Authorization": "Token 367fd78a2c51efa9c047f27121845bd90e7e5f88"})
    print(r)
    return r.status_code


# pprint.pprint(delete_item_from_list())
'''
<Response [204]>
'''


def get_pattern():
    url = 'http://127.0.0.1:8000/api/v1/pattern/'
    r = requests.get(url, headers={"Authorization": "Token 80029d4e0d7ed1833a605e00c1335db9472ef5ff"})
    print(r)
    return r.json()


# pprint.pprint(get_pattern())


def add_pattern():
    """
    <Response [201]>
    {'name': 'Test_pattern', 'url': 'http://127.0.0.1:8000/api/v1/pattern/1/'}
    """
    url = 'http://127.0.0.1:8000/api/v1/pattern/'
    r = requests.post(url, headers={"Authorization": "Token 80029d4e0d7ed1833a605e00c1335db9472ef5ff"}, json={
        'name': 'Test_pattern',
        'mobile_id': 117117
    })
    print(r)
    return r.json()

# pprint.pprint(add_pattern())


def add_item_in_pattern():
    url = f'http://{TEST_URL}/api/v1/pattern_item/'
    r = requests.post(url, headers={"Authorization": "Token 80029d4e0d7ed1833a605e00c1335db9472ef5ff"}, json={
        'item': 'Water',
        'pattern': 'Test_pattern',
        'deleted': False,
        'quantity': 6,
        'unit': 'шт'
    })
    print(r)
    return r.json()
# pprint.pprint(add_item_in_pattern())


def update_item_in_pattern():
    url = 'http://127.0.0.1:8000/api/v1/pattern_item/3/'
    r = requests.patch(url, headers={"Authorization": TEST_TOKEN}, json={
        'deleted': True,
    })
    print(r)
    return r.json()
# pprint.pprint(update_item_in_pattern())


def delete_item_from_pattern():
    url = 'http://127.0.0.1:8000/api/v1/pattern_item/3/'
    r = requests.delete(url, headers={"Authorization": TEST_TOKEN})
    print(r)
    return r.status_code

# pprint.pprint(delete_item_from_pattern())


def get_reciept():
    url = 'http://127.0.0.1:8000/api/v1/reciept/'
    r = requests.get(url, headers={"Authorization": "Token 80029d4e0d7ed1833a605e00c1335db9472ef5ff"})
    print(r)
    return r.json()


pprint.pprint(get_reciept())


def add_reciept():
    """
    <Response [201]>
    {'name': 'Test_pattern', 'url': 'http://127.0.0.1:8000/api/v1/pattern/1/'}
    """
    url = 'http://127.0.0.1:8000/api/v1/reciept/'
    r = requests.post(url, headers={"Authorization": "Token 80029d4e0d7ed1833a605e00c1335db9472ef5ff"}, json={
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