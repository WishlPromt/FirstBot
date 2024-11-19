import time, json
from random import randint

def load_base(chat_id):
    with open('credits_base.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
        return base[chat_id]


def save_base(base, chat_id):
    full_base = open('credits_base.json', 'r', encoding='utf-8')
    full_base[chat_id] = base
    with open('credits_base.json', 'w', encoding='utf-8') as file:
        json.dump(full_base, file, indent=4, ensure_ascii=False)
        file.close()


def convert_time(datetime):
    return time.strftime('%H:%M:%S %d.%m.%Y', time.localtime(datetime))

def get_message_data(data):
    id = str(data.from_user.id)
    chat_id = data.chat.id
    username = data.from_user.username
    name = data.from_user.first_name
    if username == None:
        username = name
    try:
        datetime = data.date
    except:
        datetime = 0

    return {'id': id,
            'chat_id': chat_id,
            'username': username,
            'datetime': datetime,
            'name': name}


def generate_id(ids, id, rare):
    while id in ids:
        g_id = ''
        if rare == 'regular':
            id = 're'
        elif rare == 'rare':
            id = 'ra'
        elif rare == 'epic':
            id = 'e'
        else:
            id = ''

        for i in range(randint(3, 5)):
            g_id += str(randint(0, 9))

        id += g_id

    return id

