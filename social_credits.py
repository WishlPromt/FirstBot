import json
from random import randint
from system import convert_time


with open("credits_base.json", "r", encoding="utf-8") as file:
    base = json.load(file)

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
                  'cards': {'Обычные': [], 'Редкие': [], 'Эпические': [], 'Легендарные': []},
                  'new_cards': [],
                  'cur_card': 0}


def save_base():
    file = open('credits_base.json', 'w', encoding='utf-8')
    json.dump(base, file, indent=4, ensure_ascii=False)
    file.close()


def new_id(user: dict):
    if user['username'] =='null':
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
                            'Легендарные': []
                        },
                        'new_cards': [],
                        'cur_card': 0
                        }
    save_base()


def check_user(user: dict):
    if user['id'] not in base and user['id'] != "7179420529":
        new_id(user)

    if user['id'] != "7179420529":
        for parameter in all_parameters.keys():
            if parameter not in base[user['id']].keys():
                base[user['id']][parameter] = all_parameters[parameter]
                save_base()


def add_credits(user: dict, credits):
    check_user(user)
    id = user['id']
    base[id]['credits'] = base[id]['credits'] + credits
    save_base()


def work(user: dict):
    check_user(user)
    id = user['id']
    datetime = user['datetime']
    lock_data = base[id]['time']

    credits = randint(30, 45)


    if datetime >= lock_data:

        add_credits(user, credits)
        now = datetime + 7200
        base[id]['time'] = now

        save_base()

        return f'Вы заработали <b>{credits}</b> кредитов!\nВы сможете воркать снова только <i>{convert_time(base[id]["time"])}</i>'

    else:
        return f'Не так быстро!\n Вы сможете снова воркать только <b>{convert_time(base[id]["time"])}</b>'


def collect(user: dict):
    check_user(user)
    id = user['id']
    datetime = user['datetime']
    lock_data = base[id]['collect_time']

    collects = ''
    credit_collects = 0

    if datetime >= lock_data:
        for item in base[id]['inventory']:
            item_collect = items[item][4]
            if item_collect != 'None':

                if item_collect != 'random':
                    add_credits(user, item_collect)
                    credit_collects += item_collect

                else:
                    item_collect = randint(-25, 60)
                    add_credits(user, item_collect)
                    credit_collects += item_collect

                collects += f'<b>{item}</b> - <b>{item_collect}</b> кредитов\n'

        now = datetime + 14400
        base[id]['collect_time'] = now
        save_base()

        return f'{collects} \nВы сможете собрать кредиты снова только <i>{convert_time(base[id]["collect_time"])}</i>'

    return f'Не так быстро!\n Вы сможете снова собрать кредиты только <b>{convert_time(base[id]["collect_time"])}</b>'


def balance(user: dict):
    check_user(user)
    id = user['id']

    return f'<b>{base[id]["username"]}</b>\n Ваши социальные кредиты:\n <b>{str(base[id]["credits"])}</b>'


def show_credits():
    credits = 'Социальные кредиты участников'
    for id in base.keys():
        credits += '\n' + str(base[id]['username']) + ': ' + str(base[id]['credits'])
    return credits

