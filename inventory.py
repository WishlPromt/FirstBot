import json
from social_credits import check_user


def load_base(chat_id):
    with open('credits_base.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
        return base[chat_id]


def load_items_base():
    with open('items.json', 'r', encoding='utf-8') as file:
        items_base = json.load(file)
        return items_base


def show_inventory(user):
    check_user(user)
    base = load_base(user['chat_id'])
    items_base = load_items_base()

    id = user['id']
    username = base[id]['username']
    inventory = base[id]['inventory']
    cards_packs = base[id]['cards_packs']

    if inventory != []:
        text = f'<b>{username}</b>, вот ваш инвентарь: \n'

        for item in inventory:
            if item not in ['Пак карточек']:
                text += f'<b>{item}</b>\n {items_base[item][3]}\n {items_base[item][1]}\n'

            else:
                text += f'<b>{item} - x{cards_packs[item]}</b>\n Предмет\n {items_base[item][1]}\n'

        return text

    else:
        return f'<b>{username}</b>, ваш инвентарь <b>пуст</b>\n /shop для покупки предметов и ролей'
