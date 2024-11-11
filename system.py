import time, json


def load_base():
    with open("credits_base.json", "r", encoding="utf-8") as file:
        base = json.load(file)
        return base


def save_base(base):
    file = open('credits_base.json', 'w', encoding='utf-8')
    json.dump(base, file, indent=4, ensure_ascii=False)
    file.close()


def convert_time(datetime):
    return time.strftime('%H:%M:%S %d.%m.%Y', time.localtime(datetime))


def check_chat_id(chat_id):

    base = load_base()

    if chat_id not in base:
        base[chat_id] = {}
        save_base(base)


def get_message_data(data, chat_id=''):
    if chat_id == '':
        chat_id = str(data.chat.id)
    print(chat_id)
    check_chat_id(chat_id)

    id = str(data.from_user.id)
    username = data.from_user.username
    name = data.from_user.first_name
    if username == 'null':
        username = name
    try:
        datetime = data.date
    except:
        datetime = 0

    return {'chat_id': str(chat_id),
            'id': id,
            'username': username,
            'datetime': datetime,
            'name': name}
