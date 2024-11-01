import json
from random import randint
import datetime


with open("credits_base.json", "r", encoding="utf-8") as file:
    base = json.load(file)


def get_datetime(lock):
    now = datetime.datetime.now().strftime('%d-%H')
    now = now.split('-')

    day = now[0]
    hour = now[1]

    if day[0] == '0':
        day[1:]
    if hour[1] == '0':
        hour[1:]

    if int(hour) + lock < 24:
        hour = str(int(hour) + 2)

    else:
        hour = str(int(hour) - (24-lock))
        day = str(int(day) + 1)

    if len(day) < 2:
        day == '0'+ day
    if len(hour) < 2:
        hour == '0' + hour

    now = day + '-' + hour

    return now

def get_data():
    now = datetime.datetime.now().strftime('%d-%H')
    now = now.split('-')

    day = now[0]
    hour = now[1]

    if day[0] == '0':
        day = day[1:]
    if hour[1] == '0':
        hour = hour[1:]

    return [day, hour]


def save_base():
    file = open('credits_base.json', 'w', encoding='utf-8')
    json.dump(base, file, indent=4, ensure_ascii=False)
    file.close()

def new_id(user: dict):
    base[user['id']] = {'username': user['username'],
                        'credits': 0,
                        'time': ''}
    save_base()


def add_credits(user: dict, credits):
    id = user['id']
    if id not in base:
        new_id(user)
    base[id]['credits'] = base[id]['credits'] + credits
    save_base()


def work(user: dict):
    id = user['id']
    credits = randint(30, 45)
    if id not in base:
        new_id(user)

    cur_data = get_data()

    lock_data = base[id]['time']
    hour = 0
    day = 0
    if lock_data != '':
        lock_data = lock_data.split('-')
        day = lock_data[0]
        hour = lock_data[1]

        if day[0] == '0':
            day = day[1:]
        if hour[1] == '0':
            hour = hour[1:]


    if int(cur_data[1]) >= int(hour) or int(cur_data[0]) > int(day):

        add_credits(user, credits)
        now = get_datetime(2)
        base[id]['time'] = now

        save_base()

        return f'Вы заработали {credits} кредитов!'

    else:
        return f'Не так быстро!\n Вы сможете снова воркать только в {base[id]["time"][-2:]} часов'


def show_credits():
    credits = 'Социальные кредиты участников'
    for id in base.keys():
        credits += '\n' + str(base[id]['username']) + ': ' + str(base[id]['credits'])
    return credits

