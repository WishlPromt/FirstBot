import json
from random import randint
from system import convert_time


with open("credits_base.json", "r", encoding="utf-8") as file:
    base = json.load(file)


def save_base():
    file = open('credits_base.json', 'w', encoding='utf-8')
    json.dump(base, file, indent=4, ensure_ascii=False)
    file.close()


def new_id(user: dict):
    base[user['id']] = {'username': user['username'],
                        'credits': 0,
                        'time': 0,
                        "inventory": []}
    save_base()


def check_user(user: dict):
    if user['id'] not in base:
        new_id(user)


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


def balance(user: dict):
    check_user(user)
    id = user['id']

    return f'<b>{base[id]["username"]}</b>\n Ваши социальные кредиты:\n <b>{str(base[id]["credits"])}</b>'


def show_credits():
    credits = 'Социальные кредиты участников'
    for id in base.keys():
        credits += '\n' + str(base[id]['username']) + ': ' + str(base[id]['credits'])
    return credits

