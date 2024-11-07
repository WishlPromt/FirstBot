import time, json

def load_base():
    with open('credits_base.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
        return base

def convert_time(datetime):
    return time.strftime('%H:%M:%S %d.%m.%Y', time.localtime(datetime))

def get_message_data(data):
    id = str(data.from_user.id)
    username = data.from_user.username
    name = data.from_user.first_name
    if username == 'null':
        username = name
    try:
        datetime = data.date
    except:
        datetime = 0

    return {'id': id,
            'username': username,
            'datetime': datetime,
            'name': name}

