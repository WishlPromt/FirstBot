import json
from random import randint
from system import convert_time, load_base, save_base


with open("items.json", "r", encoding="utf-8") as file:
    items = json.load(file)


all_parameters = {'credits': 0,
                  'time': 0,
                  'collect_time': 0,
                  'inventory': [],
                  'favorite_item': '',
                  'role': '',
                  'favorite_card': '',
                  'cards_packs': {'Пак карточек': 0, 'Коробка карточек': 0},
                  'cards': {'Обычные': [], 'Редкие': [], 'Эпические': [], 'Легендарные': [], 'Секретные': []},
                  'new_cards': [],
                  'cur_card': 0,
                  'max_pages': 1}


def new_id(user: dict):
    base = load_base(user['chat_id'])
    if user['username'] == None:
        user['username'] = user['name']
    base[user['id']] = {'username': user['username'],
                        'credits': 0,
                        'time': 0,
                        'collect_time': 0,
                        'inventory': [],
                        'cards_packs': {
                            'Пак карточек': 0,
                            'Коробка карточек': 0
                        },
                        "favorite_item": "Нет предмета",
                        "role": "Нет роли",
                        "favorite_card": "Нет карты",
                        'cards': {
                            'Обычные': [],
                            'Редкие': [],
                            'Эпические': [],
                            'Легендарные': [],
                            'Секретные': []
                        },
                        'new_cards': [],
                        'cur_card': 0,
                        'max_pages': 1
                        }
    save_base(base, user['chat_id'])


def check_user(user: dict):
    base = load_base(user['chat_id'])
    if user['id'] not in base and user['id'] != "7179420529":
        new_id(user)
    base = load_base(user['chat_id'])
    if user['id'] != "7179420529":
        for parameter in all_parameters.keys():
            if parameter not in base[user['id']].keys():
                base[user['id']][parameter] = all_parameters[parameter]
                save_base(base, user['chat_id'])


def add_credits(user: dict, credits):
    check_user(user)
    base = load_base(user['chat_id'])
    id = user['id']
    base[id]['credits'] = base[id]['credits'] + credits
    save_base(base, user['chat_id'])


def work(user: dict):
    check_user(user)
    base = load_base(user['chat_id'])
    id = user['id']
    datetime = user['datetime']
    lock_data = base[id]['time']

    credits = randint(30, 45)
    if 'Boss of the gym' in base[id]['inventory']:
        credits += int(credits / 100 * 50)

    if datetime >= lock_data:

        add_credits(user, credits)
        lock = 7200
        if 'Липовый модератор' in base[id]['inventory']:
            lock -= int(lock / 100 * 25)

        base = load_base(user['chat_id'])
        base[id]['time'] = datetime + lock

        save_base(base, user['chat_id'])

        return f'Вы заработали <b>{credits}</b> кредитов!\nВы сможете воркать снова только <i>{convert_time(base[id]["time"])}</i>'

    else:
        return f'Не так быстро!\n Вы сможете снова воркать только <b>{convert_time(base[id]["time"])}</b>'


def collect(user: dict):
    check_user(user)
    base = load_base(user['chat_id'])
    id = user['id']
    datetime = user['datetime']
    lock_data = base[id]['collect_time']

    collects = ''
    credit_collects = 0

    if not base[id]['inventory']:
        return f'Ваш инвентарь пуст!\nВы можете пополнить его в /shop'

    if datetime >= lock_data:
        for item in base[id]['inventory']:
            item_collect = items[item][3]
            if item_collect != 'None':

                if item_collect != 'random':
                    add_credits(user, item_collect)
                    credit_collects += item_collect

                else:
                    item_collect = randint(-25, 60)
                    add_credits(user, item_collect)
                    credit_collects += item_collect

                collects += f'<b>{item}</b>: <b>{item_collect}</b> кредитов\n'

        lock = 28800
        if 'Липовый модератор' in base[id]['inventory']:
            lock -= int(lock / 100 * 25)
        base = load_base(user['chat_id'])
        base[id]['collect_time'] = datetime + lock
        save_base(base, user['chat_id'])

        return f'Всего: <b>{credit_collects}</b> кредитов\n{collects} \nВы сможете собрать кредиты снова только <i>{convert_time(base[id]["collect_time"])}</i>'

    return f'Не так быстро!\n Вы сможете снова собрать кредиты только <b>{convert_time(base[id]["collect_time"])}</b>'


def balance(user: dict):
    check_user(user)
    base = load_base(user['chat_id'])
    id = user['id']

    return f'<b>{base[id]["username"]}</b>\n Ваши социальные кредиты:\n <b>{str(base[id]["credits"])}</b>'


def dashboard(chat_id):
    base = load_base(chat_id)
    board = 'Топ лучших пользователей чата\n'
    unsorted_users = {}

    for user in base.keys():
        if user != '7179420529':
            unsorted_users[user] = base[user]['credits']

            if base[user]['inventory']:
                for item in base[user]['inventory']:
                    unsorted_users[user] += items[item][0]

    users = sorted(unsorted_users.items(), key=lambda item: item[1], reverse=True)
    top_users = []

    if len(users) >= 10:
        for u in range(10):
            top_users.append(users[u])
    else:
        top_users = users.copy()

    if top_users:
        board = 'Топ участников чата\n'
        for user in top_users:

            id = user[0]

            inventory_sell = 0
            if base[id]['inventory']:
                for item in base[id]['inventory']:
                    inventory_sell += items[item][0]

            ofc = base[id]['favorite_card']
            fav_card = ofc[ofc.find('/')+1:ofc.find('.')]

            userboard = (f'{top_users.index(user)+1}. <b>{base[id]["username"]}</b>  -  <b>{base[id]["role"]}</b>\n'
                         f'    <b>Социальные кредиты</b>:   <b>{base[id]["credits"]}</b>\n'
                         f'    <b>Общая стоимость инвентаря</b>:   <b>{inventory_sell}</b>\n'
                         f'    <b>Любимый предмет</b>:   <b>{base[id]["favorite_item"]}</b>\n'
                         f'    <b>Любимая карточка</b>:   /{fav_card}\n\n')

            board += userboard

        return board

    return 'Дашборд пуст'

